# Copyright 2018 REMME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
import base64
from contextlib import suppress

from aiohttp_json_rpc import (
    RpcGenericServerDefinedError,
    RpcInvalidParamsError,
)
from google.protobuf.message import DecodeError
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction

from remme.shared.exceptions import ClientException
from remme.clients.account import AccountClient
from remme.clients.pub_key import PubKeyClient


__all__ = (
    'send_raw_transaction',
    'get_batch_status',
)


async def send_raw_transaction(request):
    try:
        tr = request.params[0]
    except IndexError:
        raise RpcInvalidParamsError(message='Missed protobuf')

    with suppress(Exception):
        tr = tr.encode('utf-8')

    try:
        transaction = base64.b64decode(tr)
    except Exception:
        raise RpcGenericServerDefinedError(
            error_code=-32050,
            message='Decode payload of tranasaction failed'
        )

    try:
        tr_pb = Transaction()
        tr_pb.ParseFromString(transaction)
    except DecodeError:
        raise RpcGenericServerDefinedError(
            error_code=-32050,
            message='Failed to parse transaction proto'
        )

    client = PubKeyClient()
    try:
        result = client._send_raw_transaction(tr_pb)
        return result['batch_id']
    except Exception as e:
        raise RpcGenericServerDefinedError(
            error_code=-32050,
            message=f'Send batch with transaction failed: {e}'
        )


async def get_batch_status(request):
    try:
        batch_id = request.params[0]
    except IndexError:
        raise RpcInvalidParamsError(message='Missed batch id')

    client = AccountClient()
    try:
        batch = client.get_batch(batch_id)
    except ClientException as e:
        raise RpcGenericServerDefinedError(
            error_code=-32050,
            message=f'Got error response from validator: {e}'
        )
    return batch['status']

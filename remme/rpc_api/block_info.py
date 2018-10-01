import logging

from aiohttp_json_rpc import (
    RpcGenericServerDefinedError,
    RpcInvalidParamsError,
)

from remme.clients.block_info import BlockInfoClient
from remme.shared.exceptions import KeyNotFound


__all__ = (
    'get_block_number',
    'get_blocks',
)

logger = logging.getLogger(__name__)

block_info_client = BlockInfoClient()


async def get_block_number(request):
    try:
        block_config = block_info_client.get_block_info_config()
        block_config.latest_block += 1
    except KeyNotFound:
        raise RpcGenericServerDefinedError(
            error_code=-32050,
            message='Block config not found'
        )
    else:
        return block_config.latest_block


async def get_blocks(request):
    try:
        start = request.params[0]
    except IndexError:
        raise RpcInvalidParamsError(message='Missed start')

    try:
        limit = request.params[0]
    except IndexError:
        raise RpcInvalidParamsError(message='Missed limit')

    try:
        return block_info_client.get_blocks_info(start, limit)
    except KeyNotFound:
        raise RpcGenericServerDefinedError(
            error_code=-32050,
            message='Blocks not found'
        )

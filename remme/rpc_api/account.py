import logging

from aiohttp_json_rpc import (
    RpcGenericServerDefinedError,
    RpcInvalidParamsError,
)

from remme.clients.account import AccountClient

__all__ = (
    'get_balance',
)


logger = logging.getLogger(__name__)

client = AccountClient()


async def get_balance(request):
    try:
        pub_key_user = request.params[0]
    except IndexError:
        raise RpcInvalidParamsError(message='Missed start')

    try:
        address = client.make_address_from_data(pub_key_user)
    except TypeError:
        raise RpcGenericServerDefinedError(
            error_code=-32050,
            message='Invalid public key for address creation'
        )
    logger.debug('Reading from address: {}'.format(address))
    balance = client.get_balance(address)
    return balance

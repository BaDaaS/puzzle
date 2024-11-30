from trading.exchange_api.kraken import API as KrakenAPI
from common.register import AbstractRegister


REGISTERED_APIS = AbstractRegister()
REGISTERED_APIS.register(KrakenAPI)

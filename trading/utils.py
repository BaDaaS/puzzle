from datetime import datetime
from typing import Optional
from decimal import Decimal
from common.models import Currency
from accounts.models import Account, Entity


class FIATDeposit:
    def __init__(
        self,
        currency: Currency,
        amount: Decimal,
        executed_date: datetime,
        sender: Account,
        receiver: str,
        entity: Optional[Entity],
        txid: str,
    ):
        self.txid = txid
        self.currency = currency
        self.amount = amount
        self.executed_date = executed_date
        self.sender = sender
        self.receiver = receiver
        self.entity = entity

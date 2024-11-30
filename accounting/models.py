from django.db import models
from common.models import Currency
from accounting.constants import (
    LENGTH_ADDRESS_CITY,
    LENGTH_ADDRESS_COUNTRY,
    LENGTH_EMAIL,
    LENGTH_ADDRESS_LINE,
    LENGTH_PHONE,
    LENGTH_ADDRESS_POSTAL_CODE,
    LENGTH_ADDRESS_STATE,
    LENGTH_VAT_NUMBER,
    LENGTH_WEBSITE,
    LENGTH_ENTITY_NAME,
    LENGTH_ACCOUNT_NAME,
    LENGTH_ACCOUNT_SUBTYPE,
)


class Entity(models.Model):
    name = models.CharField(unique=True, max_length=LENGTH_ENTITY_NAME)
    address_line_1 = models.CharField(
        max_length=LENGTH_ADDRESS_LINE, null=True, blank=True
    )
    address_line_2 = models.CharField(
        max_length=LENGTH_ADDRESS_LINE, null=True, blank=True
    )
    address_city = models.CharField(
        max_length=LENGTH_ADDRESS_CITY, null=True, blank=True
    )
    address_country = models.CharField(
        max_length=LENGTH_ADDRESS_COUNTRY, null=True, blank=True
    )
    address_postal_code = models.CharField(
        max_length=LENGTH_ADDRESS_POSTAL_CODE, null=True, blank=True
    )
    address_state = models.CharField(
        max_length=LENGTH_ADDRESS_STATE, null=True, blank=True
    )
    vat_number = models.CharField(
        max_length=LENGTH_VAT_NUMBER, null=True, blank=True
    )
    website = models.CharField(max_length=LENGTH_WEBSITE, null=True, blank=True)
    phone = models.CharField(max_length=LENGTH_PHONE, null=True, blank=True)
    email = models.EmailField(max_length=LENGTH_EMAIL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Entities"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Account(models.Model):
    TYPE_ASSET = "Asset"
    TYPE_LIABILITIES = "Liabilities"
    TYPE_EQUITY = "Equity"
    TYPE_REVENUE = "Revenue"
    TYPE_EXPENSES = "Expenses"
    TYPE_RECEIVABLE = "Receivable"
    TYPE_PAYABLE = "Payable"

    ACCOUNT_TYPES = [
        (TYPE_ASSET, TYPE_ASSET.upper()),
        (TYPE_LIABILITIES, TYPE_LIABILITIES.upper()),
        (TYPE_EQUITY, TYPE_EQUITY.upper()),
        (TYPE_REVENUE, TYPE_REVENUE.upper()),
        (TYPE_RECEIVABLE, TYPE_RECEIVABLE.upper()),
        (TYPE_PAYABLE, TYPE_PAYABLE.upper()),
        (TYPE_EXPENSES, TYPE_EXPENSES.upper()),
    ]

    SUBTYPE_SAVING_ACCOUNT = "SavingAccount"
    SUBTYPE_BANK = "Bank"
    SUBTYPE_CASH = "Cash"
    SUBTYPE_CREDIT_CARD = "CreditCard"
    SUBTYPE_PAYPAL = "Paypal"
    SUBTYPE_CRYPTO_EXCHANGE = "CryptoExchange"
    SUBTYPE_TRANSIT = "Transit"
    SUBTYPE_TERM_DEPOSIT_ACCOUNT = "TermDepositAccount"
    SUBTYPE_CRYPTO_WALLET = "CryptoWallet"

    SUBTYPES = [
        (SUBTYPE_SAVING_ACCOUNT, "Saving Account"),
        (SUBTYPE_BANK, "Bank"),
        (SUBTYPE_CASH, "Cash"),
        (SUBTYPE_CREDIT_CARD, "Credit card"),
        (SUBTYPE_PAYPAL, "Paypal"),
        (SUBTYPE_CRYPTO_EXCHANGE, "Crypto exchange"),
        (SUBTYPE_TRANSIT, "Transit"),
        (SUBTYPE_TERM_DEPOSIT_ACCOUNT, "Term deposit account"),
        (SUBTYPE_CRYPTO_WALLET, "Crypto wallet"),
    ]
    name = models.CharField(max_length=LENGTH_ACCOUNT_NAME, unique=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=32, choices=ACCOUNT_TYPES)
    subtype = models.CharField(
        max_length=LENGTH_ACCOUNT_SUBTYPE,
        choices=SUBTYPES,
        null=True,
        blank=True,
    )

    def is_asset(self):
        return self.account_type == self.TYPE_ASSET

    def is_liabilities(self):
        return self.account_type == self.TYPE_LIABILITIES

    def is_equity(self):
        return self.account_type == self.TYPE_EQUITY

    def is_revenue(self):
        return self.account_type == self.TYPE_REVENUE

    def is_expenses(self):
        return self.account_type == self.TYPE_EXPENSES

    def is_receivable(self):
        return self.account_type == self.TYPE_RECEIVABLE

    def is_payable(self):
        return self.account_type == self.TYPE_PAYABLE

    def is_crypto_exchange(self):
        return self.subtype == self.SUBTYPE_CRYPTO_EXCHANGE

    def is_transit(self):
        return self.subtype == self.SUBTYPE_TRANSIT

    def is_bank(self):
        return self.subtype == self.SUBTYPE_BANK

    def is_cash(self):
        return self.subtype == self.SUBTYPE_CASH

    def is_credit_card(self):
        return self.subtype == self.SUBTYPE_CREDIT_CARD

    def is_paypal(self):
        return self.subtype == self.SUBTYPE_PAYPAL

    def is_saving_account(self):
        return self.subtype == self.SUBTYPE_SAVING_ACCOUNT

    def is_crypto_wallet(self):
        return self.subtype == self.SUBTYPE_CRYPTO_WALLET

    @property
    def currency_symbol(self):
        return self.currency.symbol

    def __str__(self):
        return f"{self.name} ({self.currency_symbol} - {self.entity.name})"

    def __repr__(self):
        return f"{self.name} ({self.currency_symbol} - {self.entity.name})"

    @classmethod
    def format_transit_account(cls, currency, entity):
        return "Transit %s (%s)" % (currency.symbol, entity.name)

    @classmethod
    def format_exchange_account(cls, exchange, currency, entity):
        name = "%s %s (%s)" % (exchange.name, currency.symbol, entity.name)
        return name

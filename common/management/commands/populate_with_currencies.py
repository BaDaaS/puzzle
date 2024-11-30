from common.models import Currency
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Crypto
        Currency.objects.get_or_create(
            symbol="ALGO",
            defaults={
                "name": "Algorand",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 8,
            },
        )
        Currency.objects.get_or_create(
            symbol="USDT",
            defaults={
                "name": "Tether",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 2,
            },
        )
        Currency.objects.get_or_create(
            symbol="USDC",
            defaults={
                "name": "USD Coin",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 2,
            },
        )
        Currency.objects.get_or_create(
            symbol="BTC",
            defaults={
                "name": "Bitcoin",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 8,
            },
        )
        Currency.objects.get_or_create(
            symbol="BCH",
            defaults={
                "name": "Bitcoin Cash",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 8,
            },
        )
        Currency.objects.get_or_create(
            symbol="BSV",
            defaults={
                "name": "Bitcoin SV",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 8,
            },
        )
        Currency.objects.get_or_create(
            symbol="DUN",
            defaults={
                "name": "Dune",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 6,
            },
        )
        Currency.objects.get_or_create(
            symbol="EOS",
            defaults={
                "name": "EOS",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 8,
            },
        )
        Currency.objects.get_or_create(
            symbol="ETH",
            defaults={
                "name": "Ethereum",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="ETC",
            defaults={
                "name": "Ethereum Classic",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="LTC",
            defaults={
                "name": "Litecoin",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 8,
            },
        )
        Currency.objects.get_or_create(
            symbol="XRP",
            defaults={
                "name": "Ripple",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 8,
            },
        )
        Currency.objects.get_or_create(
            symbol="XLM",
            defaults={
                "name": "Lumen",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 8,
            },
        )
        Currency.objects.get_or_create(
            symbol="XMR",
            defaults={
                "name": "Monero",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 8,
            },
        )
        Currency.objects.get_or_create(
            symbol="XTZ",
            defaults={
                "name": "Tezos",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 6,
                "utf8_symbol": "ꜩ",
            },
        )
        Currency.objects.get_or_create(
            symbol="XTZ.S",
            defaults={
                "name": "Tezos Staking",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 6,
                "utf8_symbol": "ꜩ",
            },
        )
        Currency.objects.get_or_create(
            symbol="YEC",
            defaults={
                "name": "YCash",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 8,
            },
        )
        Currency.objects.get_or_create(
            symbol="ZEC",
            defaults={
                "name": "ZCash",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 8,
            },
        )
        # FIAT
        Currency.objects.get_or_create(
            symbol="EUR",
            defaults={
                "name": "Euro",
                "currency_type": Currency.TYPE_FIAT,
                "decimals": 5,
                "utf8_symbol": "€",
            },
        )
        Currency.objects.get_or_create(
            symbol="GBP",
            defaults={
                "name": "Pound",
                "currency_type": Currency.TYPE_FIAT,
                "decimals": 5,
                "utf8_symbol": "£",
            },
        )
        Currency.objects.get_or_create(
            symbol="USD",
            defaults={
                "name": "American dollar",
                "currency_type": Currency.TYPE_FIAT,
                "decimals": 5,
                "utf8_symbol": "$",
            },
        )
        Currency.objects.get_or_create(
            symbol="ETH.S",
            defaults={
                "name": "Ethereum Staking",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="AAVE",
            defaults={
                "name": "AAVE",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="AVAX",
            defaults={
                "name": "AVAX",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 9,
            },
        )
        Currency.objects.get_or_create(
            symbol="AXS",
            defaults={
                "name": "Axie Infinity",
                "currency_type": Currency.TYPE_CRYPTO,
                # Not sure. FIXME
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="CRV",
            defaults={
                "name": "Curve",
                "currency_type": Currency.TYPE_CRYPTO,
                # Not sure. FIXME
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="DOT",
            defaults={
                "name": "Polkadot",
                "currency_type": Currency.TYPE_CRYPTO,
                # Not sure. FIXME
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="DOT.S",
            defaults={
                "name": "Polkadot Staking",
                "currency_type": Currency.TYPE_CRYPTO,
                # Not sure. FIXME
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="SAND",
            defaults={
                "name": "Sandbox",
                "currency_type": Currency.TYPE_CRYPTO,
                # Not sure. FIXME
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="SOL",
            defaults={
                "name": "Solana",
                "currency_type": Currency.TYPE_CRYPTO,
                # Not sure. FIXME
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="SOL.S",
            defaults={
                "name": "Solana Staking",
                "currency_type": Currency.TYPE_CRYPTO,
                # Not sure. FIXME
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="LUNA",
            defaults={
                "name": "Terra Luna",
                "currency_type": Currency.TYPE_CRYPTO,
                # Not sure. FIXME
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="LUNA2",
            defaults={
                "name": "Terra Luna 2",
                "currency_type": Currency.TYPE_CRYPTO,
                # Not sure. FIXME
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="MINA",
            defaults={
                "name": "Mina",
                "currency_type": Currency.TYPE_CRYPTO,
                # Not sure. FIXME
                "decimals": 18,
            },
        )
        Currency.objects.get_or_create(
            symbol="MINA.S",
            defaults={
                "name": "Mina Staking",
                "currency_type": Currency.TYPE_CRYPTO,
                # Not sure. FIXME
                "decimals": 18,
            },
        )
        # https://optimistic.etherscan.io/token/0x4200000000000000000000000000000000000042#readContract
        Currency.objects.get_or_create(
            symbol="OP",
            defaults={
                "name": "Optimism",
                "currency_type": Currency.TYPE_CRYPTO,
                "decimals": 18,
            },
        )

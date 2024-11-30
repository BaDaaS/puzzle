from django.contrib import admin
from trading.models import Exchange, Leg, Trade
from trading.forms import TradeForm


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class LegAdmin(admin.ModelAdmin):
    list_display = (
        "leg_type",
        "get_trade_id",
        "currency",
        "amount",
        "exchange",
    )

    def get_trade_id(self, obj):
        return obj.trade.trade_id

    get_trade_id.short_description = "Trade ID"


class TradeAdmin(admin.ModelAdmin):
    form = TradeForm

    list_display = (
        "trade_id",
        "volume",
        "quantity",
        "price",
        "executed_date",
        "get_side",
        "exchange",
        "instrument",
        "base_currency",
        "counter_currency",
        "fees_quantity",
        "fees_currency",
        "entity",
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("base_currency")
            .select_related("counter_currency")
            .select_related("fees_currency")
            .select_related("entity")
            .select_related("exchange")
        )

    list_filter = ("exchange", "base_currency", "counter_currency", "entity")

    def get_side(self, obj):
        if obj.side == Trade.SIDE_BUY:
            return "Buy"
        elif obj.side == Trade.SIDE_SELL:
            return "Sell"
        raise RuntimeError("Impossible to get a string representation")

    get_side.short_description = "Side"


admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Leg, LegAdmin)
admin.site.register(Trade, TradeAdmin)

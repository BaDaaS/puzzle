from django.forms import ChoiceField, ModelForm
from trading.models import Trade


class TradeForm(ModelForm):
    side_choices = [
        (Trade.SIDE_BUY, "Buy"),
        (Trade.SIDE_SELL, "Sell"),
    ]
    side = ChoiceField(required=True, choices=side_choices)

    class Meta:
        model = Trade
        fields = "__all__"

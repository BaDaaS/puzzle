from django.contrib import admin
from common.models import Currency


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("symbol", "name", "currency_type", "decimals")
    search_fields = ("symbol",)


admin.site.register(Currency, CurrencyAdmin)

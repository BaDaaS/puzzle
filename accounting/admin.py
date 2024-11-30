from django.contrib import admin
from django.utils.html import format_html
from accounting.models import Account, Entity


class EntityAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "vat_number", "website")
    search_fields = ("name",)

    @admin.display(empty_value="N/A")
    def address(self, obj):
        """
        TODO: improve rendering
        """
        line_1 = obj.address_line_1 or ""
        line_2 = obj.address_line_2 or ""
        city = obj.address_city or ""
        state = obj.address_state or ""
        postal_code = obj.address_postal_code or ""
        country = obj.address_country or ""
        d_str = f"{line_1}<br /> {line_2},<br /> {city}, {state}<br /> {postal_code}, {country}"
        return format_html(d_str)

    address.short_description = "Address"


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_entity_name",
        "get_currency_symbol",
        "account_type",
        "subtype",
    )
    list_filter = ("entity", "subtype", "currency", "account_type")
    search_fields = ("name",)

    def get_entity_name(self, obj):
        return obj.entity.name

    def get_currency_symbol(self, obj):
        return obj.currency_symbol

    get_entity_name.short_description = "Entity"
    get_currency_symbol.short_description = "Currency"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("currency")
            .select_related("entity")
        )


admin.site.register(Account, AccountAdmin)
admin.site.register(Entity, EntityAdmin)

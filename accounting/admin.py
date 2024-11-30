from django.contrib import admin
from django.utils.html import format_html
from accounting.models import Entity


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


admin.site.register(Entity, EntityAdmin)

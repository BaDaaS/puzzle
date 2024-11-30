from django.db import models
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

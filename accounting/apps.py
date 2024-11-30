from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounting"

    def ready(self):
        from accounting.cache import load_cache

        load_cache()

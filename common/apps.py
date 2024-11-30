from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "common"

    def ready(self):
        from common.cache import load_cache

        load_cache()

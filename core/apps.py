from django.apps import AppConfig
from django.db.models.functions import Lower, Upper
from django.contrib.postgres.fields import DecimalRangeField


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self) -> None:
        DecimalRangeField.register_lookup(Lower)
        DecimalRangeField.register_lookup(Upper)

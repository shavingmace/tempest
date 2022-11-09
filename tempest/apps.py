from django.apps import AppConfig
from .forecastUpdater import *


class TempestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tempest'
    def ready(self):
        update()

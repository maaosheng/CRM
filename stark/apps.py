
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
class MyadminConfig(AppConfig):
    name = 'stark'


    def ready(self):
        autodiscover_modules('stark')


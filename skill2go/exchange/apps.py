# apps.py (in your 'exchange' app)
from django.apps import AppConfig

class ExchangeConfig(AppConfig):
    name = 'exchange'

    def ready(self):
        import exchange.signals  # Connect the signals

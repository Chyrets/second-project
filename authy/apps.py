from django.apps import AppConfig


class AuthyConfig(AppConfig):
    name = 'authy'

    def ready(self):
        import authy.signals

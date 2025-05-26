from django.apps import AppConfig


class SistemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sistem'

    def ready(self):
        import sistem.signals
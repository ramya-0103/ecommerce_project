# store/apps.py

from django.apps import AppConfig

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    # Register signals when the app is ready
    def ready(self):
        import store.signals
from django.apps import AppConfig
from django.core.cache import cache


class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'

    def ready(self):
        # Clear cache on app startup to ensure fresh start
        cache.clear()

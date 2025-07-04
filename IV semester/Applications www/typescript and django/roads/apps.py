from django.apps import AppConfig


class RoadsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "roads"

    def ready(self):
        import roads.signals

# common/apps.py
from django.apps import AppConfig

class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'

    def ready(self):
        # Auto-create groups
        from django.contrib.auth.models import Group
        for group_name in ["admin", "staff", "viewer"]:
            Group.objects.get_or_create(name=group_name)

        # Import signals
        import common.signals
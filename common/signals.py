from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    """
    Automatically assign a new user to 'viewer' group.
    Admin users (superuser) are not modified.
    """
    if created and not instance.is_superuser:
        viewer_group, _ = Group.objects.get_or_create(name="viewer")
        instance.groups.add(viewer_group)

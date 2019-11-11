from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Notes, Groups


@receiver([post_save, post_delete], sender=Notes)
def update_cache_notes(sender, **kwargs):
    cache_key = 'all_pub_notes'
    data = Notes.objects.all().order_by('group', '-created').filter(public=True)
    cache.set(cache_key, data, 3600)


@receiver([post_save, post_delete], sender=Groups)
def update_cache_groups(sender, **kwargs):
    cache_key = 'all_pub_groups'
    data = Groups.objects.all().order_by('order')
    cache.set(cache_key, data, 3600)

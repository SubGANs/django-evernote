from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='split')
def slpit_filter(value, arg):
    return value.split(arg)


@register.filter(name='in_group')
def in_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()

# accounts/templatetags/user_filters.py

from django import template

register = template.Library()


@register.filter(name='is_member')
def is_member(user, group_name):
    return user.groups.filter(name=group_name).exists()

from django import template

register = template.Library()

@register.filter
def is_in_group(user, group_name):
    return user.groups.filter(name='sellers').exists() if user.is_authenticated else False
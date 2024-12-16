from django import template

register = template.Library()

@register.filter
def is_in_group_seller(user, group_name):
    return user.groups.filter(name='sellers').exists() if user.is_authenticated else False


@register.filter
def is_in_group_customer(user, group_name):
    return user.groups.filter(name='customers').exists() if user.is_authenticated else False
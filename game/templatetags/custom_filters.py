from django import template

register = template.Library()

@register.filter
def first_name(value):
    """
    Returns the first word of the string value.
    """
    if not value:
        return ''
    return value.split()[0]

from django import template

register = template.Library()

@register.filter
def attr(obj, attr_name):
    """
    Custom template filter to access an object's attribute dynamically.
    """
    return getattr(obj, attr_name, None)

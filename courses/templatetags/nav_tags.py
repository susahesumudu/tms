# exercises/templatetags/nav_tags.py

from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag
def is_active(request, namespace, url_short_name):
    """
    Returns 'active' if the current URL matches the given namespace and url_short_name.
    Otherwise, returns an empty string.
    """
    resolver_match = resolve(request.path)
    if resolver_match.namespace == namespace and resolver_match.url_name == url_short_name:
        return 'active'
    return ''

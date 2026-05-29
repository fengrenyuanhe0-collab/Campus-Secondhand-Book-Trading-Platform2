"""
book_filters.py — Custom Django template filters for the books app
自定义模板过滤器
"""
from django import template

register = template.Library()


@register.filter
def modulo(value, arg):
    """Return value % arg — used for assigning auto-cover gradient colors"""
    try:
        return int(value) % int(arg)
    except (ValueError, ZeroDivisionError):
        return 0

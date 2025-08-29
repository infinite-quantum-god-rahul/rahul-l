# companies/templatetags/obj_extras.py
from django import template
register = template.Library()

@register.filter
def attr(obj, name):
    try:
        return getattr(obj, name)
    except Exception:
        return ""

@register.filter
def getattr(obj, path):
    try:
        cur = obj
        for part in path.split("__"):
            cur = getattr(cur, part)
        return cur
    except Exception:
        return ""

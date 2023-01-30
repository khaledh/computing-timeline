from datetime import datetime

from django import template

register = template.Library()


@register.filter
def decade(dt: datetime):
    return dt.year - dt.year % 10

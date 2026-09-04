from django import template
import jdatetime
from django.utils import timezone

register = template.Library()


@register.filter
def jalali_date(value):
    if not value:
        return ""

    try:
        value = timezone.localtime(value)
        date = jdatetime.datetime.fromgregorian(datetime=value)
        return date.strftime("%Y/%m/%d - %H:%M")
    except (ValueError, TypeError):
        return value

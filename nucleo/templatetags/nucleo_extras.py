from django import template
from django.conf import settings
from django.template import loader
from django.templatetags.static import static

register = template.Library()

@register.assignment_tag
def full_url_static(path):
    url = static(path)
    return '{}{}'.format(settings.PROTOCOL, url) if not settings.PROTOCOL else url
from django import template
from django.conf import settings
from django.template import loader

register = template.Library()

@register.assignment_tag
def pagseguro_directpayment():
    return 'https://stc.sandbox.pagseguro.uol.com.br/pagseguro/api/v2/checkout/pagseguro.directpayment.js' if settings.PAGSEGURO_SANDBOX else 'https://stc.pagseguro.uol.com.br/pagseguro/api/v2/checkout/pagseguro.directpayment.js'
from django.conf import settings


def taxa(request):
    return {
        'TAXA': settings.TAXA,
        'TAXA_VERBOSE': settings.TAXA_VERBOSE
    }
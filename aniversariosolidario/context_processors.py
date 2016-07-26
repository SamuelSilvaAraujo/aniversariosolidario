from django.conf import settings


def taxa(request):
    return {
        'TAXA': settings.TAXA,
        'TAXA_VERBOSE': settings.TAXA_VERBOSE
    }

def debug(request):
    return {
        'DEBUG': settings.DEBUG,
    }

def full_urls(request):
    return {
        'STATIC_FULL_URL': settings.STATIC_FULL_URL,
        'MEDIA_FULL_URL': settings.MEDIA_FULL_URL,
    }
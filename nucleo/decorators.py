from functools import wraps

from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse

from nucleo.models import Missao

def missao_acesso(view):
    @wraps(view)
    def inner(request, slug, *args, **kwargs):
        missao = get_object_or_404(Missao, slug=slug, usuario=request.user)
        return view(request, missao, *args, **kwargs)
    return inner

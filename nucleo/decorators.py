from functools import wraps

from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse

from nucleo.models import Missao

def acesso_view(view):
    @wraps(view)
    def inner(request, slug, *args, **kwargs):
        missao = get_object_or_404(Missao, slug=slug)
        if missao.usuario != request.user:
            return redirect(reverse('nucleo:view_not_found'))
        return view(request, slug, *args, **kwargs)
    return inner

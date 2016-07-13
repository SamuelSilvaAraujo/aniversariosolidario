# coding=utf-8
from functools import wraps

from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages


from nucleo.models import Missao, Aniversario

def missao_acesso(view):
    @wraps(view)
    def inner(request, slug, *args, **kwargs):
        missao = get_object_or_404(Missao, slug=slug, usuario=request.user)
        return view(request, missao, *args, **kwargs)
    return inner

def aniversario_finalizado(view):
    @wraps(view)
    def inner(request, *args, **kwargs):
        aniversario = get_object_or_404(Aniversario, usuario=request.user)
        if aniversario.finalizado:
            messages.error(request, 'Aniversário Solidário já foi finalizado. Por isso você não editar mais nenhuma informação!')
            return redirect(reverse('usuarios:index'))
        return view(request, *args, **kwargs)
    return inner
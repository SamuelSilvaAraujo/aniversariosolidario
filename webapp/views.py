# coding=utf-8
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from nucleo.models import Aniversario, Doacao
from pagseguro.api import PagSeguroApi


def index(request):
    aniversarios = Aniversario.objects.filter(finalizado__isnull=True)
    return render(request, 'webapp/index.html', {
        'aniversarios': aniversarios
    })

def styleguide(request):
    return render(request, 'webapp/styleguide.html')

def termos_uso(request):
    return render(request, 'webapp/termos_uso.html')

def retorno_doacao(request):
    pagseguro_api = PagSeguroApi()
    get_transaction = pagseguro_api.get_transaction(request.GET.get('transaction'))
    if not get_transaction.get('success'):
        raise Http404('A transação não foi localizada no PagSeguro')
    transaction = get_transaction.get('transaction')
    reference = transaction.get('reference')
    doacao = get_object_or_404(Doacao, id=int(reference))
    return redirect(reverse('aniversario:doacao_realizada', kwargs={
        'slug_usuario': doacao.aniversario.usuario.slug,
        'slug_missao': doacao.aniversario.missao.slug
    }))

def raisee(request):
    raise

def error404(request):
    return render(request, '404.html')
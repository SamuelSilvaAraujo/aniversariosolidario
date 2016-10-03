# coding=utf-8
from django.core.urlresolvers import reverse
from django.db.models import Sum, CharField
from django.db.models.expressions import Value
from django.db.models.functions import Concat
from django.db.models.query_utils import Q
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from nucleo.models import Aniversario, Doacao
from pagseguro.api import PagSeguroApi


def index(request):
    aniversarios = Aniversario.objects.filter(
        finalizado__isnull=True
    ).exclude(
        Q(
            ano__lt=timezone.now().year
        ) | Q(
            usuario__data_de_nascimento__month__lt=timezone.now().month,
            ano=timezone.now().year
        ) | Q(
            usuario__data_de_nascimento__day__lt=timezone.now().day,
            usuario__data_de_nascimento__month=timezone.now().month,
            ano=timezone.now().year
        )
    )

    aniversarios_realizados = Aniversario.objects.filter(
        finalizado__isnull=False,
        missao__meta__gte=1,
        doacoes__pagamento__status__in=['pago', 'disponivel']
    ).annotate(
        total_doacoes=Sum('doacoes__pagamento__valor')
    ).order_by('-total_doacoes')[:9]

    return render(request, 'webapp/index.html', {
        'aniversarios': aniversarios,
        'aniversarios_realizados': aniversarios_realizados
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

def error500(request):
    return render(request, '500.html')
# coding=utf-8
from django.core.urlresolvers import reverse
from django.db.models import Sum, CharField
from django.db.models.expressions import Value
from django.db.models.functions import Concat
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from nucleo.models import Aniversario, Doacao
from pagseguro.api import PagSeguroApi


def index(request):
    aniversarios = Aniversario.objects.filter(
        finalizado__isnull=True
    )
    try:
        aniversarios = aniversarios.annotate(
            data_de_nascimento=Concat(
                'usuario__data_de_nascimento',
                Value(''),
                output_field=CharField()
            )
        ).extra(
            select={
                'birthmonth': 'MONTH(data_de_nascimento)'
            }
        ).order_by(
            'ano', 'birthmonth'
        )
        aniversarios.count()
    except:
        aniversarios = Aniversario.objects.filter(
            finalizado__isnull=True
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
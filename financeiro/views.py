# coding=utf-8
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse

from financeiro.forms import TransacaoForm, UsuarioCompletoForm
from nucleo.models import Aniversario, Doacao

from pagseguro.api import PagSeguroApiTransparent, PagSeguroItem, PagSeguroApi
from pagseguro.models import Checkout


@login_required
def transacao(request, ano):
    aniversario = get_object_or_404(Aniversario, usuario=request.user, ano=ano)
    transacao_form = TransacaoForm(aniversario, request.POST or None, initial={'valor': aniversario.meta_de_direito_disponivel})
    if transacao_form.is_valid():
        form = transacao_form.save(commit=False)
        form.aniversario = aniversario
        form.save()
        messages.success(request, 'Solicitação de transação enviada com sucesso!')
        return redirect(reverse('usuarios:aniversarios_passados'))
    return render(request, 'financeiro/transacao.html', {
        'form':transacao_form
    })

@login_required
def efetuar_pagamento(request, doacao_id):
    doacao = get_object_or_404(Doacao, id=doacao_id, usuario=request.user)
    usuario_form = UsuarioCompletoForm(request.POST or None, instance=request.user)
    pagseguro = None
    if usuario_form.is_valid():
        request.user = usuario_form.save()
        pagseguro_api = PagSeguroApiTransparent()
        pagseguro_data = pagseguro_api.get_session_id()
        pagseguro = {
            'session_id': pagseguro_data.get('session_id')
        }
    return render(request, 'financeiro/efetuar_pagamento.html', {
        'doacao': doacao,
        'usuario_form': usuario_form,
        'pagseguro': pagseguro
    })

@login_required
def completar_pagamento(request, doacao_id):
    if not request.method == 'POST':
        return redirect(reverse('financeiro:doacao_pagamento:index', kwargs={'doacao_id': doacao_id}))

    print request.POST
    doacao = get_object_or_404(Doacao, id=doacao_id, usuario=request.user)

    payment_method = request.POST.get('payment_method')
    pagseguro_item = PagSeguroItem(
        id=str(doacao.aniversario.id),
        description=str(doacao),
        amount='%.2f' % float(doacao.pagamento.valor),
        quantity=1
    )

    if payment_method == 'pagseguro':
        pagseguro_api = PagSeguroApi(
            reference=str(doacao.id)
        )
        pagseguro_api.add_item(pagseguro_item)
        pagseguro_data = pagseguro_api.checkout()
        doacao.pagamento.checkout = Checkout.objects.get(code=pagseguro_data.get('code'))
        doacao.pagamento.save(update_fields=['checkout'])
        return redirect(pagseguro_data.get('redirect_url'))

    sender = {
        'name': request.user.nome,
        'area_code': request.user.telefone_ddd,
        'phone': request.user.telefone_numero,
        'email': request.user.email,
        'cpf': request.user.cleaned_cpf
    }

    pagseguro_api = PagSeguroApiTransparent(
        reference=str(doacao.id)
    )
    pagseguro_api.add_item(pagseguro_item)
    pagseguro_api.set_sender(**sender)
    pagseguro_api.set_shipping(
        street=request.POST.get('endereco-lagradouro'),
        number=int(request.POST.get('endereco-numero')),
        complement=request.POST.get('endereco-complemento'),
        district=request.POST.get('endereco-estado'),
        postal_code=request.POST.get('endereco-cep'),
        city=request.POST.get('endereco-cidade'),
        state=request.POST.get('endereco-estado'),
        country='BRA',
    )
    pagseguro_api.set_payment_method(payment_method)
    pagseguro_api.set_sender_hash(request.POST.get('sender_hash'))

    if payment_method == 'boleto':
        pagseguro_data = pagseguro_api.checkout()
        doacao.pagamento.boleto_link = pagseguro_data.get('transaction').get('paymentLink')
        doacao.pagamento.save(update_fields=['boleto_link'])
        return redirect(reverse('financeiro:doacao_pagamento:gerar_boleto', kwargs={'doacao_id': doacao.id}))
    if payment_method == 'creditcard':
        return

    raise Http404()

@login_required
def gerar_boleto(request, doacao_id):
    doacao = get_object_or_404(Doacao, id=doacao_id, usuario=request.user)
    return render(request, 'financeiro/gerar_boleto.html', {
        'doacao': doacao
    })
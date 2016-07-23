# coding=utf-8

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse

from financeiro.forms import TransacaoForm, UsuarioCompletoForm
from nucleo.models import Aniversario, Doacao

from pagseguro.api import PagSeguroApiTransparent, PagSeguroItem


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
    doacao = get_object_or_404(Doacao, id=doacao_id)
    usuario_form = UsuarioCompletoForm(request.POST or None, instance=request.user)
    pagseguro = None
    if usuario_form.is_valid():
        request.user = usuario_form.save()
        pagseguro_api = PagSeguroApiTransparent(
            reference=str(doacao.id)
        )
        pagseguro_data = pagseguro_api.get_session_id()
        pagseguro_item = PagSeguroItem(
            id=str(doacao.aniversario.id),
            description=str(doacao),
            amount='%.2f' % float(doacao.pagamento.valor),
            quantity=1
        )
        pagseguro_api.add_item(pagseguro_item)
        pagseguro = {
            'session_id': pagseguro_data.get('session_id')
        }
    return render(request, 'financeiro/efetuar_pagamento.html', {
        'doacao': doacao,
        'usuario_form': usuario_form,
        'pagseguro': pagseguro
    })
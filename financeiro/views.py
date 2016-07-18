# coding=utf-8

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse

from financeiro.forms import TransacaoForm
from nucleo.models import Aniversario

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
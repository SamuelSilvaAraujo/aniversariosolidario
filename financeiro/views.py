# coding=utf-8
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse

from financeiro.forms import TransacaoForm, UsuarioCompletoForm
from financeiro.models import Endereco
from nucleo.models import Aniversario, Doacao

from pagseguro.api import PagSeguroApiTransparent, PagSeguroItem, PagSeguroApi
from pagseguro.models import Checkout


@login_required
def transacao(request, ano):
    aniversario = get_object_or_404(Aniversario, usuario=request.user, ano=ano)
    if aniversario.meta_de_direito_disponivel == 0:
        messages.error(request, 'Você não tem valor disponível para retirada!')
        return redirect(reverse('usuarios:aniversarios_passados'))
    transacao_form = TransacaoForm(aniversario, request.POST or None, initial={'valor': aniversario.meta_de_direito_disponivel})
    if transacao_form.is_valid():
        form = transacao_form.save(commit=False)
        form.aniversario = aniversario
        form.save()
        messages.success(request, 'Solicitação de transação enviada com sucesso! Iremos entrar em contato via e-mail em breve, aguarde.')
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

    endereco = None

    if request.POST.get('endereco') == 'novo':
        endereco = Endereco.objects.create(
            usuario=request.user,
            lagradouro=request.POST.get('endereco-lagradouro'),
            numero=int(request.POST.get('endereco-numero')),
            complemento=request.POST.get('endereco-complemento'),
            bairro=request.POST.get('endereco-bairro'),
            cep=request.POST.get('endereco-cep'),
            cidade=request.POST.get('endereco-cidade'),
            estado=request.POST.get('endereco-estado')
        )
    else:
        endereco = Endereco.objects.get(
            usuario=request.user,
            id=int(request.POST.get('endereco'))
        )


    if endereco:
        pagseguro_api = PagSeguroApiTransparent(
            reference=str(doacao.id)
        )
        pagseguro_api.add_item(pagseguro_item)
        pagseguro_api.set_sender(**sender)
        pagseguro_api.set_shipping(**endereco.pagseguro_serialize())
        pagseguro_api.set_payment_method(payment_method)
        pagseguro_api.set_sender_hash(request.POST.get('sender_hash'))

        if payment_method == 'boleto':
            pagseguro_data = pagseguro_api.checkout()
            doacao.pagamento.boleto_link = pagseguro_data.get('transaction').get('paymentLink')
            doacao.pagamento.save(update_fields=['boleto_link'])
            return redirect(reverse('financeiro:doacao_pagamento:gerar_boleto', kwargs={'doacao_id': doacao.id}))
        if payment_method == 'creditcard':
            pagseguro_api.set_creditcard_token(request.POST.get('card_token'))
            pagseguro_api.set_creditcard_data(
                quantity=1,
                value='%.2f' % doacao.pagamento.valor,
                name=request.POST.get('nome-no-cartao'),
                birth_date=request.POST.get('data-nascimento-cartao'),
                cpf=request.POST.get('cpf-cartao'),
                area_code=request.POST.get('telefone-ddd'),
                phone=request.POST.get('telefone')
            )

            endereco_cartao = None
            endereco_cartao_opt = request.POST.get('endereco-cartao')
            if endereco_cartao_opt == 'mesmo':
                endereco_cartao = endereco
            elif endereco_cartao_opt == 'novo':
                endereco_cartao = Endereco.objects.create(
                    usuario=request.user,
                    lagradouro=request.POST.get('endereco-cartao-lagradouro'),
                    numero=int(request.POST.get('endereco-cartao-numero')),
                    complemento=request.POST.get('endereco-cartao-complemento'),
                    bairro=request.POST.get('endereco-cartao-bairro'),
                    cep=request.POST.get('endereco-cartao-cep'),
                    cidade=request.POST.get('endereco-cartao-cidade'),
                    estado=request.POST.get('endereco-cartao-estado')
                )
            else:
                endereco_cartao = Endereco.objects.get(
                    usuario=request.user,
                    id=int(request.POST.get('endereco-cartao'))
                )
            pagseguro_api.set_creditcard_billing_address(**endereco_cartao.pagseguro_serialize())

            pagseguro_data = pagseguro_api.checkout()
            doacao.pagamento.cartao = Checkout.objects.get(code=pagseguro_data.get('code'))
            doacao.pagamento.save(update_fields=['cartao'])
            return redirect(reverse('aniversario:doacao_realizada', kwargs={
                'slug_usuario': doacao.aniversario.usuario.slug,
                'slug_missao': doacao.aniversario.missao.slug
            }))

    raise Http404()

@login_required
def gerar_boleto(request, doacao_id):
    doacao = get_object_or_404(Doacao, id=doacao_id, usuario=request.user)
    return render(request, 'financeiro/gerar_boleto.html', {
        'doacao': doacao
    })
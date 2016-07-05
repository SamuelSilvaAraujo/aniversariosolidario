# coding=utf-8
import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import ConfirmacaoDeEmail

from .forms import CadastroFrom, LoginForm, AlterarFotoForm

@login_required
def index(request):
    return render(request, 'usuarios/index.html')

def cadastro(request):
    form = CadastroFrom(request.POST or None)
    if form.is_valid():
        usuario = form.save()
        usuario.set_password(form.cleaned_data.get('password'))
        usuario.save()
        usuario.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, usuario)
        return redirect(request.GET.get('next', reverse('usuarios:index')))
    return render(request, 'usuarios/cadastro.html', {
        'form': form
    })

def entrar(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        login(request, form.usuario)
        return redirect(reverse('usuarios:index'))
    return render(request, 'usuarios/login.html', {
        'form': form
    })

@login_required
def sair(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta com sucesso!')
    return redirect(reverse('usuarios:login'))

@login_required
def reenviar_email_de_confirmacao(request):
    ultimo_pedido = request.user.confirmacoes_de_email.all().last()
    if not ultimo_pedido or ultimo_pedido.data_solicitacao - datetime.timedelta(minutes=40) > timezone.now():
        ConfirmacaoDeEmail.objects.create(usuario=request.user)
        messages.success(request, 'E-mail de confirmação reenviado com sucesso!')
    else:
        messages.error(request, 'Você fez um pedido para reenvio do e-mail de confirmação faz pouco tempo.')
    return redirect(reverse('usuarios:index'))

@login_required
def confirmar_email(request, chave):
    confirmacao_de_email = get_object_or_404(ConfirmacaoDeEmail, chave=chave)
    if request.user != confirmacao_de_email.usuario:
        raise Http404()
    if not request.user.data_ativacao_email:
        request.user.data_ativacao_email = timezone.now()
        request.user.save(update_fields=['data_ativacao_email'])
        messages.success(request, 'E-mail confirmado com sucesso!')
    request.user.confirmacoes_de_email.all().delete()
    return redirect(reverse('usuarios:index'))

@login_required
def alterar_foto(request):
    form = AlterarFotoForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
    return render(request, 'usuarios/alterar_foto.html', {
        'form': form
    })
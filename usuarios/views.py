# coding=utf-8
import datetime
import urllib
from tempfile import mkstemp

from os import unlink

from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.files import File
from .models import ConfirmacaoDeEmail, Usuario

from .forms import CadastroFrom, LoginForm, AlterarFotoForm, CompletarPerfilForm, AlterarPerfilForm,EditarSenhaForm,RecuperarSenhaForm, \
    LoginOuCadastroForm, AddEmailPagSeguro

from .models import RecuperarSenha

from nucleo.models import Aniversario

@login_required
def index(request):
    return render(request, 'usuarios/index.html')

@login_required
def social_login_get_avatar(request):
    user = request.user
    index = int(request.GET.get('i', '0'))
    socials = user.socialaccount_set.all()
    if socials:
        try:
            avatar_url = socials[index].get_avatar_url()
            ex = avatar_url.split('.')[-1]
            filename = 'avatar-{}.{}'.format(user.slug, ex if ex in ['jpg', 'jpeg', 'png', 'gif'] else 'jpg')
            i, temp_path = mkstemp(filename)
            urllib.urlretrieve(avatar_url, temp_path)
            file = open(temp_path)
            django_file = File(file)
            user.foto.save(filename, django_file)
            file.close()
            unlink(temp_path)
        except IndexError:
            pass
    return redirect(reverse('usuarios:index'))

def cadastro(request):
    form = CadastroFrom(request.POST or None, initial={'email': request.GET.get('email', '')})
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
    form = LoginForm(request.POST or None, initial={'email': request.GET.get('email', '')})
    if form.is_valid():
        login(request, form.usuario)
        return redirect(request.GET.get('next', reverse('usuarios:index')))
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
    if not ultimo_pedido or ultimo_pedido.data_solicitacao + datetime.timedelta(minutes=40) < timezone.now():
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

@login_required
def alterar_perfil(request):
    perfil_form = AlterarPerfilForm(request.POST or None, instance=request.user)
    if perfil_form.is_valid():
        perfil_form.save()
        messages.success(request, 'Dados atualizados com sucesso!')
    return render(request, 'usuarios/alterar_perfil.html', {
        'perfil_form': perfil_form,
    })

@login_required
def completar_perfil(request):
    empty_fields = request.user.empty_fields
    fields = request.GET.get('just_fields', '')
    if fields:
        fields = filter(lambda x: x in empty_fields, fields.split(','))
    else:
        fields = empty_fields
    if not fields:
        messages.warning(request, 'Seu perfil está completo.')
        return redirect(reverse('usuarios:index'))
    form = CompletarPerfilForm(fields, request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect(request.GET.get('next', reverse('usuarios:index')))
    return render(request, 'usuarios/completar_perfil.html', {
        'form': form
    })

@login_required
def editar_senha(request):
    usuario = request.user
    editar_form = EditarSenhaForm(request.POST or None)
    if editar_form.is_valid():
        password = editar_form.cleaned_data.get('password')
        usuario.set_password(password)
        usuario.save(update_fields=['password'])
        messages.success(request, 'Senha Alterada com sucesso!')
        usuario.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, usuario)
        return redirect(reverse('usuarios:alterar_perfil'))
    return render(request, 'usuarios/editar_senha.html', {
        'form':editar_form
    })

def recuperar_senha(request):
    form = RecuperarSenhaForm(request.POST or None)
    if form.is_valid():
        RecuperarSenha.objects.create(usuario=form.usuario)
        messages.success(request, 'Um e-mail foi enviado para {} com um link para redefinir sua senha.'.format(form.usuario.email))
        return redirect(reverse('usuarios:login'))
    return render(request, 'usuarios/recuperar_senha.html', {
        'form': form
    })

def confimar_recuperar_senha(request, chave):
    recuperar_senha_instance = get_object_or_404(RecuperarSenha, chave=chave)
    recuperar_senha_instance.usuario.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, recuperar_senha_instance.usuario)
    recuperar_senha_instance.delete()
    return redirect(reverse('usuarios:editar_senha'))

def login_ou_cadastro(request):
    form = LoginOuCadastroForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            r = reverse('usuarios:login')
        else:
            r = reverse('usuarios:cadastro')
        return redirect('{}?next={}&email={}'.format(r, request.GET.get('next', '/'), email))
    return render(request, 'usuarios/login_ou_cadastro.html', {
        'form': form
    })

@login_required
def add_email_pagseguro(request):
    form_pagseguro = AddEmailPagSeguro(request.POST or None, instance = request.user)
    if form_pagseguro.is_valid():
        form_pagseguro.save()
        return redirect(request.GET.get('next', reverse('usuarios:index')))
    return render(request, 'usuarios/aniversario_emailpagseguro.html', {
        'form':form_pagseguro
    })

@login_required
def aniversarios_passados(request):
    return render(request, 'usuarios/aniversarios_passados.html')

@login_required
def doacoes(request):
    return render(request, 'usuarios/doacoes.html')
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import CadastroFrom,LoginForm,AlterarFotoForm

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
        return redirect(reverse('usuarios:index'))
    return render(request, 'usuarios/cadastro.html', {
        'form': form
    })

def entrar(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        pass
    return render(request, 'usuarios/login.html', {
        'form': form
    })

@login_required
def alterar_foto(request):
    form = AlterarFotoForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
    return render(request, 'usuarios/alterar_foto.html', {
        'form': form
    })
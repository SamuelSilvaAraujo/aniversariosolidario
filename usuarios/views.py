from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import CadastroFrom,LoginForm

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
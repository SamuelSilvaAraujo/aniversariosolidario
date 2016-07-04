from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from .forms import CadastroFrom,LoginForm

@login_required
def index(request):
    return render(request, 'usuarios/index.html')

def cadastro(request):
    form = CadastroFrom(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, 'usuarios/cadastro.html', {
        'form': form
    })

def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        pass
    return render(request, 'usuarios/login.html', {
        'form': form
    })
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
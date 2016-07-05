from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import CadastroFrom,LoginForm,AlterarFotoForm

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

@login_required
def alterar_foto(request):
    form = AlterarFotoForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
    return render(request, 'usuarios/alterar_foto.html', {
        'form': form
    })
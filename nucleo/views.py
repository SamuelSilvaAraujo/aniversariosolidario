from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import MissaoForm
from .models import Missao

@login_required
def criar_missao(request):
    form = MissaoForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, 'nucleo/criarmissao.html', {
        'form':form
    })

@login_required
def editar_missao(request, slug):
    missao = Missao.objects.get(slug=slug)
    form = MissaoForm(request.POST or None, instance=missao)
    if form.is_valid():
        form.save()
    return render(request, 'nucleo/editar_missao.html', {
        'form': form
    })

@login_required
def missao(request,slug):
    missao = Missao.objects.get(slug=slug)
    return render(request, 'nucleo/missao.html',{'missao':missao})


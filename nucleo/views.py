from django.shortcuts import render

from .forms import MissaoForm

def criarMissao(request):
    form = MissaoForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request,'nucleo/criarmissao.html', {
        'form':form
    })
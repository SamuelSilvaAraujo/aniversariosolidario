from django.shortcuts import render
from nucleo.models import Aniversario


def index(request):
    aniversarios = Aniversario.objects.filter(finalizado__isnull=True)
    return render(request, 'webapp/index.html', {
        'aniversarios': aniversarios
    })

def styleguide(request):
    return render(request, 'webapp/styleguide.html')

def raisee(request):
    raise

def termos_uso(request):
    return render(request, 'webapp/termos_uso.html')
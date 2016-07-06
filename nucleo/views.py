from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import MissaoForm,MediaForm
from .models import Missao,Media

def iniciar_aniversario(request):
    if not request.user.is_authenticated():
        return redirect('{}?next={}'.format(reverse('usuarios:cadastro'), reverse('nucleo:iniciar_aniversario')))
    if not request.user.data_de_nascimento:
        return redirect('{}?next={}&just_fields=data_de_nascimento'.format(reverse('usuarios:completar_perfil'), reverse('nucleo:iniciar_aniversario')))
    missao_form = MissaoForm(request.POST or None)
    return render(request, 'nucleo/iniciar_aniversario.html', {
        'missao_form': missao_form
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

@login_required
def gerenciar_medias(request,slug):
    missao = Missao.objects.get(slug=slug)
    media_form = MediaForm(request.POST or None, request.FILES or None)
    if media_form.is_valid():
        arquivo = media_form.save(commit=False)
        arquivo.missao = missao
        arquivo.save()
    arquivos = Media.objects.filter(missao=missao)
    return render(request, 'nucleo/gerenciar_medias.html', {
        'form':media_form,
        'arquivos':arquivos
    })
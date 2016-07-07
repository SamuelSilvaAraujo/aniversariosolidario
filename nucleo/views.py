# coding=utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Aniversario
from .forms import MissaoForm,MediaForm
from .models import Missao,Media

def iniciar_aniversario(request):
    if not request.user.is_authenticated():
        return redirect('{}?next={}'.format(reverse('usuarios:login_ou_cadastro'), reverse('nucleo:iniciar_aniversario')))
    if not request.user.data_de_nascimento:
        return redirect('{}?next={}&just_fields=data_de_nascimento'.format(reverse('usuarios:completar_perfil'), reverse('nucleo:iniciar_aniversario')))
    if request.user.aniversario_solidario:
        messages.error(request, 'Você já tem Aniversário Solidário acontecendo!')
        return redirect(reverse('usuarios:index'))

    missao_form = MissaoForm(request.POST or None)
    if missao_form.is_valid():
        missao = missao_form.save()
        Aniversario.objects.create(
            usuario=request.user,
            missao=missao,
            ano=request.user.proximo_aniversario.year
        )
        return redirect(reverse('usuarios:index'))
    return render(request, 'nucleo/iniciar_aniversario.html', {
        'missao_form': missao_form
    })

def aniversario(request, slug_usuario, slug_missao):
    aniversario_instance = get_object_or_404(Aniversario, usuario__slug=slug_usuario, missao__slug=slug_missao)
    return render(request, 'nucleo/aniversario.html', {
        'aniversario': aniversario_instance
    })

@login_required
def editar_missao(request, slug):
    missao = get_object_or_404(Missao, slug=slug)
    form = MissaoForm(request.POST or None, instance=missao)
    if form.is_valid():
        form.save()
    return render(request, 'nucleo/editar_missao.html', {
        'form': form
    })

@login_required
def gerenciar_medias(request, slug):
    missao = get_object_or_404(Missao, slug=slug)
    act = request.POST.get('act')
    media_form = MediaForm(
        request.POST or None if act == 'add_novo' else None,
        request.FILES or None if act == 'add_novo' else None,
        prefix='add_novo'
    )

    if act:
        if act == 'add_novo' and media_form.is_valid():
            arquivo = media_form.save(commit=False)
            arquivo.missao = missao
            arquivo.save()
            messages.success(request, 'Arquivo adicionado com sucesso!')
            return redirect(reverse('nucleo:missao:medias', kwargs={'slug': missao.slug}))

        if 'editar_' in act:
            media_id = int(act.split('_')[-1])
            for media in missao.medias.all():
                if media.id == media_id:
                    media.editar_form(request.POST or None)
                    if media.get_editar_form.is_valid():
                        media.get_editar_form.save()

    return render(request, 'nucleo/gerenciar_medias.html', {
        'form': media_form,
        'missao': missao
    })

@login_required
def gerenciar_medias_action(request, slug, media_id, action):
    media = get_object_or_404(Media, missao__slug=slug, id=media_id)
    if action == 'up':
        media.up()
    if action == 'down':
        media.down()
    if action == 'delete':
        media.delete()
    return redirect(reverse('nucleo:missao:medias', kwargs={'slug': slug}))
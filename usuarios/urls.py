from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cadastro/$', views.cadastro, name='cadastro'),
    url(r'^entrar/$', views.entrar, name='login'),
    url(r'^sair/$', views.sair, name='sair'),
    url(r'^reenviaremaildeconfirmacao/$', views.reenviar_email_de_confirmacao, name='reenviar_email_de_confirmacao'),
    url(r'^confirmaremail/(?P<chave>[A-Z]+)/$', views.confirmar_email, name='confirmar_email'),
    url(r'^alterarfoto/$', views.alterar_foto, name='alterar_foto'),
    url(r'^alterarperfil/$', views.alterar_perfil, name='alterar_perfil'),
    url(r'^completarperfil/$', views.completar_perfil, name='completar_perfil'),
    url(r'^editarsenha/$', views.editar_senha, name='editar_senha'),
    url(r'^redefinirsenha/', include([
        url(r'^$', views.recuperar_senha, name='index'),
        url(r'^(?P<chave>[A-Z]+)/$', views.confimar_recuperar_senha, name='confirmar')
    ], namespace='recuperarsenha')),
    url(r'^entraroucadastro/$', views.login_ou_cadastro, name='login_ou_cadastro'),
]
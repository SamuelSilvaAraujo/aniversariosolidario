from django.conf.urls import url, include
from . import views
from nucleo import views as nucleo_views
from financeiro import views as financeiro_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cadastro/$', views.cadastro, name='cadastro'),
    url(r'^entrar/$', views.entrar, name='login'),
    url(r'^sair/$', views.sair, name='sair'),
    url(r'^reenviaremaildeconfirmacao/$', views.reenviar_email_de_confirmacao, name='reenviar_email_de_confirmacao'),
    url(r'^confirmaremail/(?P<chave>[A-Z]+)/$', views.confirmar_email, name='confirmar_email'),
    url(r'^bemvindo/(?P<chave>[A-Z]+)/$', views.confirmar_email, name='bem_vindo'),
    url(r'^alterarfoto/$', views.alterar_foto, name='alterar_foto'),
    url(r'^alterarperfil/$', views.alterar_perfil, name='alterar_perfil'),
    url(r'^completarperfil/$', views.completar_perfil, name='completar_perfil'),
    url(r'^editarsenha/$', views.editar_senha, name='editar_senha'),
    url(r'^redefinirsenha/', include([
        url(r'^$', views.recuperar_senha, name='index'),
        url(r'^(?P<chave>[A-Z]+)/$', views.confimar_recuperar_senha, name='confirmar')
    ], namespace='recuperarsenha')),
    url(r'^entraroucadastro/$', views.login_ou_cadastro, name='login_ou_cadastro'),
    url(r'^editarapelo/$', nucleo_views.aniversario_apelo, name='aniversario_apelo'),
    url(r'^cadastraremailpagseguro/$', views.add_email_pagseguro, name='add_email_pagseguro'),
    url(r'^aniversario/(?P<ano>[\d]+)/', include([
        url(r'^retirada/$', financeiro_views.transacao, name='transacao'),
        url(r'^feedback/$', nucleo_views.feedback, name='feedback'),
    ], namespace='detalhes_aniversario')),
    url(r'^aniversarios/$', views.aniversarios_passados, name='aniversarios_passados'),
    url(r'^socialgetinfos/$', views.social_login_get_infos, name='social_login_get_infos'),
    url(r'^doacoes/$', views.doacoes, name='doacoes'),

    url(r'^export/$', views.export_dados, name='export'),
    url(r'^logarcomo/(?P<slug>[\w-]+)', views.logar_como, name='logar_como')
]
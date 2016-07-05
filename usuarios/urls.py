from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cadastro/$', views.cadastro, name='cadastro'),
    url(r'^entrar/$', views.entrar, name='login'),
    url(r'^sair/$', views.sair, name='sair'),
    url(r'^reenviaremaildeconfirmacao/$', views.reenviar_email_de_confirmacao, name='reenviar_email_de_confirmacao'),
    url(r'^confirmaremail/(?P<chave>[A-Z]+)/$', views.confirmar_email, name='confirmar_email'),
    url(r'^alterarfoto/$',views.alterar_foto,name='alterarfoto')
]
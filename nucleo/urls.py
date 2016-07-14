from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^iniciaraniversario/$', views.iniciar_aniversario, name='iniciar_aniversario'),
    url(r'^aniversariofinalizar/$', views.aniversario_finalizar, name='aniversario_finalizar'),
    url(r'^missao/(?P<slug>[\w-]+)/', include([
        url(r'^$', views.editar_missao, name='editar_missao'),
        url(r'^medias/$', views.gerenciar_medias, name='medias'),
        url(r'^media/(?P<media_id>[\d-]+)/(?P<action>[\w]+)/$', views.gerenciar_medias_action, name='medias_action')
    ], namespace='missao')),
]
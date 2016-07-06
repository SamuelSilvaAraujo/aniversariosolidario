from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^iniciaraniversario/$', views.iniciar_aniversario, name='iniciar_aniversario'),
    url(r'^missao/(?P<slug>[\w-]+)/', include([
        url(r'^$', views.missao, name='missao'),
        url(r'^editar/$', views.editar_missao, name='editar_missao'),
        url(r'^medias/$', views.gerenciar_medias, name='medias')
    ], namespace='missao')),
]
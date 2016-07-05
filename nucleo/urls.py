from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^iniciarmissao/$', views.criar_missao, name='criar_missao'),
    url(r'^missao/(?P<slug>[\w-]+)/', include([
        url(r'^$', views.missao, name='missao'),
        url(r'^editar/$', views.editar_missao, name='editar_missao'),
    ], namespace='missao')),
]
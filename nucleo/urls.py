from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^criar/$', views.criar_missao, name='criar_missao'),
    url(r'^(?P<slug>[\w-]+)/$', views.missao, name='missao'),
]
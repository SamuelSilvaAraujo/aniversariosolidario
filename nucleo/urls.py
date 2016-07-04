from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^criar/$', views.criarMissao, name='criarMissao'),
]
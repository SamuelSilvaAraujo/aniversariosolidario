from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^doacao/(?P<doacao_id>[\d]+)/', include([
        url(r'^$', views.efetuar_pagamento, name='index'),
        url(r'^completar/$', views.completar_pagamento, name='completar'),
    ], namespace='doacao_pagamento'))
]
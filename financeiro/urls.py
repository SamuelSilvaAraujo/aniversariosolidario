from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^doacao/(?P<doacao_id>[\d]+)/', include([
        url(r'^$', views.efetuar_pagamento, name='index'),
        url(r'^completar/$', views.completar_pagamento, name='completar'),
        url(r'^boleto/$', views.gerar_boleto, name='gerar_boleto'),
    ], namespace='doacao_pagamento'))
]
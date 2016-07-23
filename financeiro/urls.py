from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'efetuarpagamento/(?P<doacao_id>[\d]+)/', views.efetuar_pagamento, name='efetuar_pagamento')
]
from django.contrib import admin

from .models import Pagamento, Transacao

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    pass

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    pass
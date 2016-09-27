# coding=utf-8
from django.contrib import admin
from django.core.checks import messages

from .models import Pagamento, Transacao, Endereco


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    actions = ['enviar_email_doacao_completa']
    list_filter = ['status']

    def enviar_email_doacao_completa(self, request, queryset):
        for d in queryset:
            d.enviar_email_doacao_completa()
            self.message_user(request, 'E-mail enviado com sucesso!', level=messages.INFO)

    enviar_email_doacao_completa.short_description = 'Enviar e-mail de doação completa'

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    pass

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    pass
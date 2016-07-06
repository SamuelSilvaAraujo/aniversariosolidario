# coding=utf-8
from django.contrib import admin
from django.core.checks import messages
from .models import Email, ContaDeEmail, ConfiguracaoDeEmail


@admin.register(ContaDeEmail)
class ContaDeEmailAdmin(admin.ModelAdmin):
    actions = ['conta_de_email_test']

    def conta_de_email_test(self, request, queryset):
        for c in queryset:
            msg = None
            level = None
            if c.test():
                msg = u'Tudo OK com {}'.format(c.verbose())
                level = messages.INFO
            else:
                msg = u'Tivemos algum problema com {}'.format(c.verbose())
                level = messages.ERROR
            if msg:
                self.message_user(request, msg, level=level)
    conta_de_email_test.short_description = 'Testar Conexão'

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'processado']
    readonly_fields = ['chave', 'processado', 'enviado']
    actions = ['processar_email']

    def processar_email(self, request, queryset):
        for e in queryset:
            if e.processado:
                self.message_user(request, u'{} já foi processado'.format(e), level=messages.ERROR)
            else:
                e.processar()
    processar_email.short_description = 'Processar'

@admin.register(ConfiguracaoDeEmail)
class ConfiguracaoDeEmailAdmin(admin.ModelAdmin):
    pass
from django.contrib import admin
from .models import Usuario, ConfirmacaoDeEmail, RecuperarSenha

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields


class UsuarioResource(resources.ModelResource):
    teste = fields.Field(column_name='teste')
    class Meta:
        model = Usuario
        fields = ('nome', 'data_de_nascimento', 'email', 'telefone_ddd', 'telefone_numero')

@admin.register(Usuario)
class UsuarioAdmin(ImportExportModelAdmin):
    pass

@admin.register(ConfirmacaoDeEmail)
class ConfirmacaoDeEmailAdmin(admin.ModelAdmin):
    pass

@admin.register(RecuperarSenha)
class RecuperarSenhaAdmin(admin.ModelAdmin):
    pass
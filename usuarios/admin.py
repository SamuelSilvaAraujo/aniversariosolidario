from django.contrib import admin
from .models import Usuario, ConfirmacaoDeEmail, RecuperarSenha

from import_export import resources

class UsuarioResource(resources.ModelResource):
    class Meta:
        model = Usuario
        fields = ('nome', 'data_de_nascimento', 'email', 'telefone_ddd', 'telefone_numero')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass

@admin.register(ConfirmacaoDeEmail)
class ConfirmacaoDeEmailAdmin(admin.ModelAdmin):
    pass

@admin.register(RecuperarSenha)
class RecuperarSenhaAdmin(admin.ModelAdmin):
    pass
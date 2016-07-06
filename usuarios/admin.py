from django.contrib import admin
from .models import Usuario, ConfirmacaoDeEmail, RecuperarSenha


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass

@admin.register(ConfirmacaoDeEmail)
class ConfirmacaoDeEmailAdmin(admin.ModelAdmin):
    pass

@admin.register(RecuperarSenha)
class RecuperarSenhaAdmin(admin.ModelAdmin):
    pass
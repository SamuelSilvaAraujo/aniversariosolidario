from django.contrib import admin
from .models import Usuario, ConfirmacaoDeEmail


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass

@admin.register(ConfirmacaoDeEmail)
class ConfirmacaoDeEmailAdmin(admin.ModelAdmin):
    pass
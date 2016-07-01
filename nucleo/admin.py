from django.contrib import admin
from .models import Missao,Aniversario,Doacao,Media


@admin.register(Missao)
class MissaoAdmin(admin.ModelAdmin):
    pass

@admin.register(Aniversario)
class AniversarioAdmin(admin.ModelAdmin):
    pass

@admin.register(Doacao)
class DoacaoAdmin(admin.ModelAdmin):
    pass

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass
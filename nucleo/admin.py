from django.contrib import admin
from .models import Missao,Aniversario,Doacao,Media


@admin.register(Missao,Aniversario,Doacao,Media)

class MissaoAdmin(admin.ModelAdmin):
    pass

class AniversarioAdmin(admin.ModelAdmin):
    pass

class DoacaoAdmin(admin.ModelAdmin):
    pass

class MediaAdmin(admin.ModelAdmin):
    pass
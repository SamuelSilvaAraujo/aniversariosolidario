from django.contrib import admin
from nucleo.models import Missao


@admin.register(Missao)
class MissaoAdmin(admin.ModelAdmin):
    pass
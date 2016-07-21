from django.contrib import admin
from .models import Missao, Aniversario, Doacao, Media, Feedback
from ordered_model.admin import OrderedModelAdmin


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
class MediaAdmin(OrderedModelAdmin):
    list_display = ['__str__', 'move_up_down_links']

@admin.register(Feedback)
class FeedblackAdmin(admin.ModelAdmin):
    pass
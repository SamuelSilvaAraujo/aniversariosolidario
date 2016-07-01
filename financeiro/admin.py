from django.contrib import admin

from .models import Pagamento

@admin.register(Pagamento)

class PagamentoAdmin(admin.ModelAdmin):
    pass
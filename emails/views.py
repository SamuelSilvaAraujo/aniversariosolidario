from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from emails.models import ConfiguracaoDeEmail


def cancelar_envio_de_emails(request, chave):
    config_de_email = get_object_or_404(ConfiguracaoDeEmail, chave=chave)
    if request.method == 'POST':
        if not config_de_email.cancelado_as:
            config_de_email.cancelado_as = timezone.now()
            config_de_email.save(update_fields=['cancelado_as'])
        messages.success(request, 'Envios cancelados com sucesso.')
    return render(request, 'emails/cancelar_envio_de_emails.html', {
        'config_de_email': config_de_email
    })
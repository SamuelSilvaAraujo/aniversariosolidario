from time import sleep
from django.core.management.base import BaseCommand
from emails.models import Email


class Command(BaseCommand):
    help = 'Processa os e-mails'

    def handle(self, *args, **options):
        while True:
            for email in Email.objects.filter(processado__isnull=True):
                print email, email.processar()
                sleep(1)
            sleep(3)
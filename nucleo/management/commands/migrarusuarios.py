# coding=utf-8
import requests

from django.core.management import BaseCommand
from django.utils import timezone
from usuarios.models import Usuario

JSON_URL = 'http://localhost:8100/XOQM/'
# JSON_URL = 'http://o.aniversariosolidario.com/XOQM/'

class Command(BaseCommand):
    help = 'Migrar usuários da plataforma antiga'

    def handle(self, *args, **options):
        j = requests.get(JSON_URL).json()
        usuarios = j.get('usuarios')
        for u in usuarios:
            usuario = None
            try:
                usuario = Usuario.objects.get(email=u.get('email'))
            except Usuario.DoesNotExist:
                pass

            if not usuario:
                print(u)
                usuario = Usuario.objects.create(
                    email=u.get('email'),
                    nome=u.get('nome'),
                    data_de_nascimento=u.get('data_nascimento'),
                    password=u.get('password'),
                    migrado=True,
                    data_ativacao_email=timezone.now()
                )
                if u.get('foto'):
                    usuario.set_foto_from_url(u.get('foto'))

            print(usuario)
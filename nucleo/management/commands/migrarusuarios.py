# coding=utf-8
import requests

from django.core.management import BaseCommand
from usuarios.models import Usuario

JSON_URL = 'http://172.16.194.92:8080/XOQM/'
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
                    migrado=True
                )
                if u.get('foto'):
                    usuario.set_foto_from_url(u.get('foto'))

            print(usuario)
            usuario.delete()
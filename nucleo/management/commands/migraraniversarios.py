import requests

import os
import urllib
from tempfile import mkstemp

from django.core.management import BaseCommand
from django.core.files import File

from usuarios.models import Usuario
from nucleo.models import Missao, Aniversario, Media


JSON_URL = 'http://localhost:8100/XOQAN/'
# JSON_URL = 'http://o.aniversariosolidario.com/XOQAN/'

class Command(BaseCommand):
    help = 'Migrar aniversarios da plataforma antiga'

    def handle(self, *args, **options):
        j = requests.get(JSON_URL).json()
        aniversarios = j.get('anivesarios')
        missoes = j.get('missoes')
        medias = j.get('medias')
        for m in missoes:
            usuario = None
            try:
                usuario = Usuario.objects.get(email=m.get('usuario'))
            except Usuario.DoesNotExist:
                pass

            if usuario:
                print m
                Missao.objects.create(
                    usuario = usuario,
                    titulo = m.get('titulo'),
                    descricao = m.get('descricao'),
                    slug = m.get('slug'),
                    meta = m.get('meta'),
                    beneficiado = m.get('beneficiado'),
                )
        for a in aniversarios:
            usuario = None
            try:
                usuario = Usuario.objects.get(email=a.get('usuario'))
            except Usuario.DoesNotExist:
                pass

            if usuario:
                print a
                Aniversario.objects.create(
                    usuario = usuario,
                    missao = Missao.objects.get(slug=a.get('missao')),
                    ano = a.get('ano'),
                    apelo = a.get('apelo'),
                    finalizado = a.get('finalizado')
                )

        for me in medias:
            missao = Missao.objects.get(slug=me.get('missao'))
            media = Media.objects.create(
                missao = missao,
                descricao = me.get('descricao'),
            )
            print me
            if me.get('arquivo'):
                url = me.get('arquivo')
                ex = url.split('.')[-1]
                filename = 'avatar-{}.{}'.format(missao.usuario.slug, ex if ex in ['jpg', 'jpeg', 'png', 'gif'] else 'jpg')
                i, temp_path = mkstemp(filename)
                urllib.urlretrieve(url, temp_path)
                file = open(temp_path)
                django_file = File(file)
                media.arquivo.save(filename, django_file)
                file.close()
                os.unlink(temp_path)
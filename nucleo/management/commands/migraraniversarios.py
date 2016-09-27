import requests

import os
import urllib
from tempfile import mkstemp

from django.core.management import BaseCommand
from django.core.files import File

from usuarios.models import Usuario
from nucleo.models import Missao, Aniversario, Media, Doador, Doacao
from financeiro.models import Pagamento


# JSON_URL = 'http://localhost:8100/XOQAN/'
JSON_URL = 'http://o.aniversariosolidario.com/XOQAN/'

class Command(BaseCommand):
    help = 'Migrar aniversarios da plataforma antiga'

    def handle(self, *args, **options):
        j = requests.get(JSON_URL).json()
        aniversarios = j.get('anivesarios')
        missoes = j.get('missoes')
        medias = j.get('medias')
        doadores = j.get('doadores')
        doacoes = j.get('doacoes')
        pagamentos = j.get('pagamentos')

        for doador in doadores:
            Doador.objects.create(
                nome = doador.get('nome'),
                email = doador.get('email')
            )
            print doador

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
                aniversario = Aniversario.objects.create(
                    usuario = usuario,
                    missao = Missao.objects.get(slug=a.get('missao')),
                    ano = a.get('ano'),
                    apelo = a.get('apelo'),
                    finalizado = a.get('finalizado')
                )
                for doacao in doacoes:
                    if a.get('id') == doacao.get('aniversario'):
                        usuario = None
                        doador = None
                        try:
                            usuario = Usuario.objects.get(email=doacao.get('usuario'))
                            doador = Doador.objects.get(email=doacao.get('doador'))
                        except Usuario.DoesNotExist:
                            pass
                        except Doador.DoesNotExist:
                            pass

                        status_dict = {
                            0: 'em_analise',
                            1: 'aguardando',
                            2: 'pago',
                            3: 'disponivel',
                            4: 'em_disputa',
                            5: 'devolvido',
                            6: 'cancelado',
                        }

                        pagamento = Pagamento.objects.create(
                            valor = doacao.get('valor'),
                            status = status_dict[doacao.get('status')]
                        )
                        d = Doacao.objects.create(
                            aniversario = aniversario,
                            usuario = usuario,
                            doador = doador,
                            pagamento = pagamento
                        )
                        d.data = doacao.get('data')
                        d.save(update_fields=['data'])
                        print doacao
                print a

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
                filename = '{}.{}'.format(me.get('descricao'), ex if ex in ['jpg', 'jpeg', 'png', 'gif'] else 'jpg')
                i, temp_path = mkstemp(filename)
                urllib.urlretrieve(url, temp_path)
                file = open(temp_path)
                django_file = File(file)
                media.arquivo.save(filename, django_file)
                file.close()
                os.unlink(temp_path)
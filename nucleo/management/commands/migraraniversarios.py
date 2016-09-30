import requests

import os
import urllib
from tempfile import mkstemp

from django.core.management import BaseCommand
from django.core.files import File
from django.utils import timezone

from dateutil import parser

from usuarios.models import Usuario
from nucleo.models import Missao, Aniversario, Media, Doador, Doacao
from financeiro.models import Pagamento, Transacao


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

        for d in doadores:
            doador = None
            try:
                doador = Doador.objects.get(email=d.get('email'), nome=d.get('nome'))
            except Doador.DoesNotExist:
                pass

            if not doador:
                Doador.objects.create(
                    nome = d.get('nome'),
                    email = d.get('email')
                )
            print d

        for m in missoes:
            missao = None

            try:
                missao = Missao.objects.get(slug=m.get('slug'))
            except Missao.DoesNotExist:
                pass

            if not missao:
                usuario = None

                try:
                    usuario = Usuario.objects.get(email=m.get('usuario'))
                except Usuario.DoesNotExist:
                    pass

                if usuario:
                    Missao.objects.create(
                        usuario = usuario,
                        titulo = m.get('titulo'),
                        descricao = m.get('descricao'),
                        slug = m.get('slug'),
                        meta = m.get('meta'),
                        beneficiado = m.get('beneficiado'),
                    )
            print m

        for a in aniversarios:
            usuario = None

            try:
                usuario = Usuario.objects.get(email=a.get('usuario'))
            except Usuario.DoesNotExist:
                pass

            if usuario:
                aniversario = None

                try:
                    aniversario = Aniversario.objects.get(ano=a.get('ano'), usuario=usuario)
                except Aniversario.DoesNotExist:
                    pass

                if not aniversario:
                    aniversario = Aniversario.objects.create(
                        usuario=Usuario.objects.get(email=a.get('usuario')),
                        missao=Missao.objects.get(slug=a.get('missao')),
                        ano=a.get('ano'),
                        apelo=a.get('apelo'),
                        finalizado=a.get('finalizado')
                    )

                    for d in doacoes:

                        if a.get('id') == d.get('aniversario'):
                            doacao = None

                            try:
                                doacao = Doacao.objects.get(aniversario=aniversario, data=d.get('data'), pagamento__valor=d.get('valor'))
                            except Doacao.DoesNotExist:
                                pass

                            if not doacao:
                                usuario = None
                                doador = None

                                try:
                                    usuario = Usuario.objects.get(email=d.get('usuario'))
                                except Usuario.DoesNotExist:
                                    pass

                                try:
                                    doador = Doador.objects.get(email=d.get('doador_email'), nome=d.get('doador_nome'))
                                except Doador.DoesNotExist:
                                    pass

                                status_dict = {
                                    0: 'em_analise',
                                    1: 'aguardando',
                                    2: 'disponivel',
                                    3: 'disponivel',
                                    4: 'em_disputa',
                                    5: 'devolvido',
                                    6: 'cancelado',
                                }
                                pagamento = Pagamento.objects.create(
                                    valor=d.get('valor'),
                                    status=status_dict[d.get('status')]
                                )

                                do = Doacao.objects.create(
                                    aniversario = aniversario,
                                    usuario = usuario,
                                    doador = doador,
                                    pagamento = pagamento
                                )
                                do.data = d.get('data')
                                do.save(update_fields=['data'])
                                print d

                    if aniversario.meta_atingida > 0:
                        t = Transacao.objects.create(
                            aniversario = aniversario,
                            valor = aniversario.meta_de_direito_disponivel,
                            data_realizacao = timezone.now(),
                        )
                        t.taxa_atual = .17
                        t.save(update_fields=['taxa_atual'])
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
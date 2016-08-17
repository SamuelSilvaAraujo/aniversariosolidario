from django.contrib.sitemaps import Sitemap
from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from nucleo.models import Aniversario


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return ['index', 'termos_uso', 'usuarios:cadastro', 'usuarios:login']

    def location(self, item):
        return reverse(item)

class AniversarioSolidarioSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Aniversario.objects.all()

    def location(self, item):
        return reverse('aniversario:index', kwargs={
            'slug_usuario': item.usuario.slug,
            'slug_missao': item.missao.slug
        })
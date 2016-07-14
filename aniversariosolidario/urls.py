from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from usuarios import urls as usuarios_urls
from nucleo import urls as nucleo_urls
from webapp import views as webapp_views
from emails import views as emails_views
from nucleo import views as nucleo_views
from pagseguro import urls as pagseguro_urls

urlpatterns = [
    url(r'^$', webapp_views.index, name='index'),
    url(r'^termosdeuso/$', webapp_views.termos_uso, name='termos_uso'),
    url(r'^styleguide/$', webapp_views.styleguide, name='styleguide'),
    url(r'^raise/$', webapp_views.raisee, name='raisee'),
    url(r'^cancelarenviodeemails/(?P<chave>[A-Z]+)/$', emails_views.cancelar_envio_de_emails, name='cancelar_envio_de_emails'),

    url(r'^usuario/', include(usuarios_urls, namespace='usuarios')),
    url(r'^', include(nucleo_urls, namespace='nucleo')),
    url(r'^admin/', admin.site.urls),
    url(r'^retorno/pagseguro/', include(pagseguro_urls)),
    url(r'^(?P<slug_usuario>[\w-]+)/(?P<slug_missao>[\w-]+)/', include([
        url(r'^$', nucleo_views.aniversario, name='index'),
        url(r'^doar/$', nucleo_views.aniversario_doar, name='doar'),
        url(r'^doacaorealizada/$', nucleo_views.aniversario_doacao_realizada, name='aniversario_doacao_realizada'),
    ], namespace='aniversario')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
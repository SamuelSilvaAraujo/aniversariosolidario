from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from usuarios import urls as usuarios_urls
from nucleo import urls as nucleo_urls
from webapp import views as webapp_views
from emails import views as emails_views

urlpatterns = [
    url(r'^$', webapp_views.index, name='index'),
    url(r'^styleguide/$', webapp_views.styleguide, name='styleguide'),
    url(r'^cancelarenviodeemails/(?P<chave>[A-Z]+)/$', emails_views.cancelar_envio_de_emails, name='cancelar_envio_de_emails'),

    url(r'^usuario/', include(usuarios_urls, namespace='usuarios')),
    url(r'^', include(nucleo_urls, namespace='nucleo')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
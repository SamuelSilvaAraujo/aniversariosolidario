from django.conf.urls import url, include
from django.contrib import admin
from webapp import views as webapp_views
from usuarios import urls as usuarios_urls
from nucleo import urls as nucleo_urls

urlpatterns = [
    url(r'^$', webapp_views.index, name='index'),
    url(r'^usuario/', include(usuarios_urls, namespace='usuarios')),
    url(r'^missao/',include(nucleo_urls,namespace='nucleo')),
    url(r'^admin/', admin.site.urls),
]
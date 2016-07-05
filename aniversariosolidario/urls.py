from django.conf.urls import url, include
from django.contrib import admin
from usuarios import urls as usuarios_urls
from nucleo import urls as nucleo_urls
from webapp import views as webapp_views

urlpatterns = [
    url(r'^$', webapp_views.index, name='index'),
    url(r'^styleguide/$', webapp_views.styleguide, name='styleguide'),

    url(r'^usuario/', include(usuarios_urls, namespace='usuarios')),
    url(r'^', include(nucleo_urls, namespace='nucleo')),
    url(r'^admin/', admin.site.urls),
]
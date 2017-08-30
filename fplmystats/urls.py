from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^error/(?P<manager_error>[0-1])/(?P<league_error>[0-1])$', views.index_error, name='index_error'),
    url(r'^admin/', admin.site.urls),
    url(r'^manager/', include('manager.urls', namespace='manager')),
    url(r'^league/', include('league.urls', namespace='league')),
]

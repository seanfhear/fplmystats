from django.conf.urls import url
from . import views


urlpatterns = [
    # /league/
    url(r'^$', views.search, name='search'),

    # /league/[LEAGUE_ID]
    url(r'^(?P<league_id>[0-9]+)/$', views.detail, name='detail')
]

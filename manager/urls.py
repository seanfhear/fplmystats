from django.conf.urls import url
from . import views


urlpatterns = [
    # /manager/
    url(r'^$', views.search, name='search'),

    # /manager/[MANAGER_ID]
    url(r'^(?P<manager_id>[0-9]+)/$', views.detail, name='detail')
]

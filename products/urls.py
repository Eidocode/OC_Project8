from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<product_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^search/$', views.search, name='search'),
    url(r'^add_fav/(?P<product_id>[0-9]+)/$', views.favorite, name='favorite')
]

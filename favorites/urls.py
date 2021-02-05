from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.favorites, name='favorites'),
    url(r'^del_fav/(?P<favorite_id>[0-9]+)/$', views.remove_from_fav, name='del_fav'),
]
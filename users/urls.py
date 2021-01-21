from django.conf.urls import url, include
from django.urls import path

from . import views


urlpatterns = [
    url(r'^signup/', views.signup, name='signup'),
    url(r'^account/', views.user_account, name='user_account'),
    url(r'^favorites/', include('favorites.urls')),
]
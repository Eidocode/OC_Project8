from django.shortcuts import render
from django.contrib.auth.models import User

from products.models import Favorite


def favorites(request):
    current_user = request.user
    fav_products = Favorite.objects.all()
    fav_prod_filtered = fav_products.filter(users_id=current_user)
    context = {
        'favorites': fav_prod_filtered
    }
    return render(request, 'favorites/favorites.html', context)

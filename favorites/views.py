from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from products.models import Favorite


def favorites(request):
    current_user = request.user
    fav_products = Favorite.objects.all()
    fav_prod_filtered = fav_products.filter(users_id=current_user)

    paginator = Paginator(fav_prod_filtered, 6)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'favorites': products,
        'paginate': True,
    }
    return render(request, 'favorites/favorites.html', context)

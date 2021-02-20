from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from unidecode import unidecode

from products.models import Favorite


def favorites(request):
    """
    Used when displaying the current user's favorites
    """
    cur_user = request.user  # Gets the current logged-in user
    fav_products = Favorite.objects.all()  # Gets all "Favorite" model objects

    # Gets the favorites of the current user
    fav_prod_filtered = fav_products.filter(users_id=cur_user).order_by('-id')

    # Adds pagination for up to 6 products per page
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


def remove_from_fav(request, favorite_id):
    """
    Used when the user removes a product from his favorites
    """
    # Gets a favorite designated by favorite_id or returns 404
    favorite = get_object_or_404(Favorite, pk=favorite_id)
    favorite.delete()

    print("{}, {} a été supprimé des favoris".format(
                    favorite.products.name, favorite.products.brand))

    return redirect(request.META['HTTP_REFERER'])

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from random import randrange

from .models import Product, Category, Favorite


def index(request):
    return render(request, 'products/index.html')


def detail(request, product_id):
    substitutes = []
    current_user = request.user
    product = get_object_or_404(Product, pk=product_id)
    category = Category.objects.filter(products__id=product.id)

    all_prods = []
    for catg in category:
        prods = Product.objects.filter(categories__id=catg.id)
        for prod in prods:
            if (prod.score <= product.score):
                print(product.score + " : " + prod.score)
                all_prods.append(prod)

    nb_prod = 6
    if (len(all_prods) < nb_prod):
        nb_prod = len(all_prods)

    for i in range(nb_prod):
        index = randrange(0, len(all_prods))
        substitutes.append(all_prods.pop(index))
        i += 1

    qs_fav = Favorite.objects.filter(users__id=current_user.id)
    fav_prods_id = []
    for fav in qs_fav:
        fav_prods_id.append(fav.products.id)

    print(fav_prods_id)
    print(len(substitutes))
    context = {
        'product': product,
        'substitutes': substitutes,
        'fav_prods_id': fav_prods_id
    }

    return render(request, 'products/detail.html', context)


def favorite(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, pk=product_id)

    new_fav = Favorite(
        products=product,
        users=current_user
    )
    new_fav.save()

    print(product.name + " a été ajouté aux favoris")

    return redirect(request.META['HTTP_REFERER'])


def search(request):
    query = request.GET.get('query')

    if not query:
        products = Product.objects.all().order_by('id')
    else:
        products = Product.objects.filter(name__icontains=query).order_by('-id')
    # if not products.exists():
    #     # Recherche du nom d'une catégorie à la place d'un produit
    #     # albums = Album.objects.filter(artists__name__icontains=query)
    #     pass

    paginator = Paginator(products, 6)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    title = "Résultats de la recherche {}".format(query)
    context = {
        'products': products,
        'title': title,
        'paginate': True,
    }

    return render(request, 'products/search.html', context)

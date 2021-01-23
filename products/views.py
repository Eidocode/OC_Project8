from django.shortcuts import render, get_object_or_404

from .models import Product
from django.http import HttpResponse


def index(request):
    return render(request, 'products/index.html')


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/detail.html', context)


def search(request):
    query = request.GET.get('query')

    if not query:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(name__icontains=query)
    if not products.exists():
        # Recherche du nom d'une catégorie à la place d'un produit
        # albums = Album.objects.filter(artists__name__icontains=query)
        pass

    title = "Résultats pour la requête " + query
    context = {
        'products': products,
        'title': title
    }

    return render(request, 'products/search.html', context)

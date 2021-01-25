from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Product


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
    
    title = "Résultats de la recherche"
    context = {
        'products': products,
        'title': title,
        'query': query,
        'paginate': True,
    }

    return render(request, 'products/search.html', context)

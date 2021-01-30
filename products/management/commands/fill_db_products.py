import requests

from django.core.management.base import BaseCommand
from django.utils import timezone

from random import randrange
from math import ceil

from products.models import Category, Product


URL = 'https://fr.openfoodfacts.org/'  # /categorie/[name_cat].json

NB_CATEGORIES_TO_GET = 20
MIN_PRODUCTS_TO_FILTER = 100
PRODUCTS_PER_PAGE = 20
PRODUCTS_PER_CATG = 20

NB_TRY = 3


class Command(BaseCommand):
    help = 'Adds categories and products in pur_beurre database'

    def add_arguments(self, parser):
        parser.add_argument('nb_prod', type=int, help='Indicates the number of products by category to be created')

    def handle(self, *args, **options):
        nb_prod = options['nb_prod']
        self.stdout.write("Processing for %s products by category..." % nb_prod)
        self._get_random_products(nb_prod)

    def _get_categories_url(self):
        categories_in_db = Category.objects.all()
        categories_url = []
        for category in categories_in_db:
            categories_url.append(category.url)

        return categories_url
    
    def _get_categories_jsonid(self):
        categories_in_db = Category.objects.all()
        categories_jsonid = []
        for category in categories_in_db:
            data = {
                'id': category.id,
                'json_id': category.json_id,
            }
            categories_jsonid.append(data)

        return categories_jsonid

    def _get_products_from_url(self, url):
        try:
            url_json = requests.get(url + '.json')
            print('Connecting to {}...'.format(url))
        except requests.exceptions.ConnectionError:
            print('Unable to connect to {}, skip the category...'.format(url))
            return

        self.stdout.write("Getting products from " + url)
        json_data = url_json.json()

        nb_products = int(json_data.get('count'))
        nb_pages = ceil(nb_products / PRODUCTS_PER_PAGE)

        lst_all_prods = []
        i = 1
        for i in range(nb_pages):
            page_url = "{}/{}.json".format(url, str(i))
            json_url_products = requests.get(page_url).json()
            lst_products = json_url_products.get('products')

            for product in lst_products:
                lst_all_prods.append(product)

        return lst_all_prods

    def _get_random_products(self, nb_prod):
        categories_db_jsonid = self._get_categories_jsonid()
        products_db_barcode = self._get_products_db_barcode()
        categories_url = self._get_categories_url()

        list_rnd_products = []
        count = 0
        for url in categories_url:
            products_in_category = self._get_products_from_url(url)

            if products_in_category is None:
                continue

            print('==== {} ===='.format(url))
            print('')

            if nb_prod > len(products_in_category):
                nb_prod = len(products_in_category)
                print("Only {} products available in this category...".format(nb_prod))

            rnd_prod_catg = []
            for i in range(nb_prod):
                index = randrange(0, len(products_in_category))
                rnd_prod_catg.append(products_in_category.pop(index))
                i += 1

            list_rnd_products.append(rnd_prod_catg)

            for product in rnd_prod_catg:
                data = self.test_product_keys(product)
                if data is not None:
                    prod = Product(
                        name=data['name'],
                        brand=data['brand'],
                        description=data['description'],
                        score=data['score'],
                        barcode=data['barcode'],
                        url_img_small=data['url_img_small'],
                        url_img=data['url_img'],
                        url_off=data['url_off'],
                        url_img_nutrition=data['url_img_nutrition'],
                    )

                    if data['barcode'] not in products_db_barcode:
                        prod.save()
                    else:
                        print('{} with barcode : {} already in database'.format(data['name'], data['barcode']))
                        continue

                    for catg in categories_db_jsonid:
                        if catg['json_id'] in product['categories_tags']:
                            prod.categories.add(catg['id'])
                            print('Add relation between {} and category id {}'.format(data['name'], catg['id']))

                    count += 1
            print('')

        print(str(count) + ' viables products.')

        return list_rnd_products
        
    def test_product_keys(self, product):

        data = None
        try:
            data = {
                'name': product['product_name'],
                'brand': product['brands'],
                'description': product['ingredients_text'],
                'score': product['nutriscore_grade'],
                'barcode': product['code'],
                'categories': product['categories_tags'],
                'url_img': product['image_url'],
                'url_img_small': product['image_small_url'],
                'url_off': product['url'],
                'url_img_nutrition': product['image_nutrition_url']
            }
        except KeyError:
            print('This product is not viable')
                    
        return data
    
    def _get_products_db_barcode(self):
        products = Product.objects.all()
        products_barcode = []

        for product in products:
            products_barcode.append(product.barcode)
        
        return products_barcode

        

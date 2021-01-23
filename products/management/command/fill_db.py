import requests

from django.core.management.base import BaseCommand

from random import randrange

from products.models import Category, Product


URL = 'https://fr.openfoodfacts.org/'  # /categorie/[name_cat].json

NB_CATEGORIES_TO_GET = 20
MIN_PRODUCTS_TO_FILTER = 100
PRODUCTS_PER_PAGE = 20
PRODUCTS_PER_CATG = 20

NB_TRY = 3


class Command(BaseCommand):
    help = 'Adds categories and products in pur_beurre database'

    # def add_arguments(self, parser):
    #     parser.add_argument('nb_catg', type=int)

    def handle(self, *args, **options):
        print("HELLO")
        # nb_cats = options.get['nb_catg', None]
        # print(nb_cats)
        # return u'NB CATS: %s ' % (nb_cats)
        # self.set_categories_to_db(nb_cats)

    def _get_categories(self, min_nb_prod):
        list_cat = []
        list_cat_filtered = []

        json_cat = requests.get(URL + 'categories.json').json()
        list_cat = json_cat.get('tags')

        for category in list_cat:
            if (category['products'] >= min_nb_prod and category['id'].startswith('fr')):
                json_category = requests.get(category['url'] + '.json').json()
                nb_products = int(json_category.get('count'))
                if nb_products is not None:
                    if nb_products >= min_nb_prod:
                        list_cat_filtered.append(category)

        print("Categories >= {} product(s) : {}".format(min_nb_prod, str(len(list_cat_filtered))))

        return list_cat_filtered

    def _get_random_categories(self, nb_cat):
        categories = []
        lst = self._get_categories(MIN_PRODUCTS_TO_FILTER)

        for i in range(nb_cat):
            index = randrange(0, len(lst))
            categories.append(lst.pop(index))

        return categories

    def _compare_with_db(self, nb_cat):
        categories_list = []
        new_categories = self._get_random_categories(nb_cat)
        categories_in_db = Category.objects.all()

        for category in categories_in_db:
            # TODO A VERIFIER !!!
            if category.json_id not in new_categories['id']:
                categories_list.append(category)
            else:
                print("{} with json_id : {} already in database...".format(category.name, category.json_id))

        return categories_list

    def set_categories_to_db(self, nb_cat):
        categories = self._compare_with_db(nb_cat)

        for category in categories:
            new_category = Category(
                name=category['name'],
                json_id=category['id'],
                url=category['url']
            )
            print('Added new category : {} to database'.format(category.name))
            new_category.save()

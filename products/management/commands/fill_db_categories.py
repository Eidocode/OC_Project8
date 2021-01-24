import requests

from django.core.management.base import BaseCommand

from random import randrange

from products.models import Category


URL = 'https://fr.openfoodfacts.org/'  # /categorie/[name_cat].json

MIN_PRODUCTS_TO_FILTER = 100


class Command(BaseCommand):
    help = 'Adds categories and products in pur_beurre database'

    def add_arguments(self, parser):
        parser.add_argument('nb_catg', type=int, help='Indicates the number of categories to be created')

    def handle(self, *args, **options):
        nb_cats = options['nb_catg']
        self.stdout.write("Processing for %s categories..." % nb_cats)
        self.set_categories_to_db(nb_cats)

    def _get_categories(self, min_nb_prod):
        self.stdout.write("Getting categories containing at least %s products..." % min_nb_prod)
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
        lst = self._get_categories(MIN_PRODUCTS_TO_FILTER)
        self.stdout.write("Getting %s random categories..." % nb_cat)

        categories = []
        for i in range(nb_cat):
            index = randrange(0, len(lst))
            categories.append(lst.pop(index))

        return categories

    def _compare_with_db(self, nb_cat):
        categories_in_db = Category.objects.all()
        json_ids_in_db = []
        for category in categories_in_db:
            json_ids_in_db.append(category.json_id)

        new_categories = self._get_random_categories(nb_cat)
        self.stdout.write("Compares the selection with existing data stored in the database...")

        categories_list = []
        for category in new_categories:
            if category['id'] not in json_ids_in_db:
                categories_list.append(category)
            else:
                print("{} with json_id : {} already in database...".format(category['name'], category['id']))

        return categories_list

    def set_categories_to_db(self, nb_cat):
        categories = self._compare_with_db(nb_cat)
        self.stdout.write("Adding %s categories in the database..." % len(categories))

        for category in categories:
            new_category = Category(
                name=category['name'],
                json_id=category['id'],
                url=category['url']
            )
            print('Added new category : {} to database'.format(category['name']))
            new_category.save()

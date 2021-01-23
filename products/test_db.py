import requests

from random import randrange


URL = 'https://fr.openfoodfacts.org/'  # /categorie/[name_cat].json


def get_categories(min_nb_prod):
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


def get_random_categories(nb_cat):
    categories = []

    lst = get_categories(100)
    print("liste début : " + str(len(lst)))

    for i in range(nb_cat):
        print(str(i) + ". longueur liste boucle : " + str(len(lst)))
        index = randrange(0, len(lst))
        categories.append(lst.pop(index))

    print("liste fin : " + str(len(lst)))

    return categories


categories = get_random_categories(40)
print(str(len(categories)) + ' categories')

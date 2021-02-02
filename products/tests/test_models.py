from django.test import TestCase
from django.contrib.auth.models import User

from products.models import Category, Product, Favorite


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Setup non modified objects used for all test methods
        Category.objects.create(
            name='Pates',
            json_id='fr:pates',
            url = 'https://www.openfoodfacts.com/pates'
        )

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_json_id_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('json_id').verbose_name
        self.assertEquals(field_label, 'json id')

    def test_jsonid_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('json_id').max_length
        self.assertEquals(max_length, 200)
    
    def test_jsonid_is_unique(self):
        category = Category.objects.get(id=1)
        unique = category._meta.get_field('json_id').unique
        self.assertTrue(unique)
    
    def test_object_name_is_name(self):
        category = Category.objects.get(id=1)
        object_name = category.name
        self.assertEquals(object_name, str(category))
    

class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Setup non modified objects used for all test methods
        Product.objects.create(
            name='Saumon',
            brand='Labeyrie',
            description='Saumon fumé savoureux de Norvege',
            score='C',
            barcode='12345678910',
            url_img_small='https://www.openfoodfacts.com/poisson/saumon/url_img_small',
            url_img='https://www.openfoodfacts.com/poisson/saumon/url_img',
            url_off='https://www.openfoodfacts.com/poisson/saumon/url_off',
            url_img_nutrition = 'https://www.openfoodfacts.com/poisson/saumon/url_img_nutrition',
        )
    
    def test_name_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)
    
    def test_brand_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('brand').max_length
        self.assertEquals(max_length, 200)
    
    def test_score_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('score').max_length
        self.assertEquals(max_length, 1)
    
    def test_barcode_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('barcode').max_length
        self.assertEquals(max_length, 50)
    
    def test_barcode_is_unique(self):
        product = Product.objects.get(id=1)
        unique = product._meta.get_field('barcode').unique
        self.assertTrue(unique)
    
    def test_object_name_is_name_brand_barcode(self):
        product = Product.objects.get(id=1)
        object_name = f'{product.name}, {product.brand}, {product.barcode}'
        self.assertEquals(object_name, str(product))


class FavoriteModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def test_added_date_autonow(self):
        added_date = Favorite._meta.get_field('added_date').auto_now_add
        self.assertTrue(added_date)

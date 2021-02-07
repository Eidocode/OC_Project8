from django.test import TestCase
from django.urls import reverse

from products.forms import SearchForm
from products.models import Category, Product
from django.contrib.auth import authenticate, login


class IndexPageTestCase(TestCase):
    # Test that index page returns 200
    def test_index_url_exists_at_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_url_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_url_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'products/index.html')

    def test_index_search_form_one_char(self):
        form = SearchForm(data={'search': 'd'})
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['search'][0], 'Saisir, au minimum, deux caractères pour valider la recherche')

    def test_index_search_form_special_char(self):
        form = SearchForm(data={'search': 'recherche@'})
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['search'][0], 'Les caractères spéciaux ne sont pas autorisés')

    def test_index_search_form_with_a_quote(self):
        form = SearchForm(data={'search': "C'est une recherche"})
        self.assertTrue(form.is_valid())

    def test_index_search_form_number(self):
        form = SearchForm(data={'search': 'recherche1'})
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['search'][0], 'Les chiffres ne sont pas autorisés')


class SearchPageTestCase(TestCase):
    # Test that search page returns 200
    def test_search_url_exists_at_location(self):
        response = self.client.get('/products/search/?search=test')
        self.assertEqual(response.status_code, 200)

    # Test that a research returns 200
    def test_search_url_by_name(self):
        response = self.client.get(reverse('search')+'?search=test')
        self.assertEqual(response.status_code, 200)

    # Test that a bad research returns 404
    def test_bad_search_url_returns_404(self):
        response = self.client.get(reverse('search')+'search=test')
        self.assertEqual(response.status_code, 404)

    def test_search_url_uses_correct_template(self):
        response = self.client.get(reverse('search')+'?search=test')
        self.assertTemplateUsed(response, 'products/search.html')

    def test_pagination_is_true(self):
        response = self.client.get(reverse('search')+'?search=test')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('paginate' in response.context)
        self.assertTrue(response.context['paginate'] is True)


class ResultPageTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Setup non modified objects used for all test methods
        number_of_products = 20

        category = Category(
            name='Category',
            json_id='fr:category',
            url='https://www.openfoodfacts.com/category',
        )
        category.save()

        for pnum in range(number_of_products):
            prod = Product(
                name=f'Product {pnum}',
                brand=f'Brand {pnum}',
                description='Product Description',
                score='B',
                barcode=f'12345678910 {pnum}',
                url_img_small=f'https://www.openfoodfacts.com/category/product/url_img_small {pnum}',
                url_img=f'https://www.openfoodfacts.com/category/product/url_img {pnum}',
                url_off=f'https://www.openfoodfacts.com/category/product/url_off {pnum}',
                url_img_nutrition=f'https://www.openfoodfacts.com/category/product/url_img_nutrition {pnum}',
            )
            prod.save()
            prod.categories.add(category.id)

    def test_result_url_exists_at_location(self):
        response = self.client.get('/products/5/')
        self.assertEqual(response.status_code, 200)

    def test_result_url_by_name(self):
        response = self.client.get(reverse('result', kwargs={'product_id': 5}))
        self.assertEqual(response.status_code, 200)

    def test_bad_search_url_returns_404(self):
        response = self.client.get(reverse('result', kwargs={'product_id': 100}))
        self.assertEqual(response.status_code, 404)

    def test_search_url_uses_correct_template(self):
        response = self.client.get(reverse('result', kwargs={'product_id': 5}))
        self.assertTemplateUsed(response, 'products/result.html')

    def test_search_url_proposes_6_substitutes(self):
        response = self.client.get(reverse('result', kwargs={'product_id': 5}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('substitutes' in response.context)
        self.assertTrue(len(response.context['substitutes']) == 6)

    def test_detail_url_exists_at_location(self):
        response = self.client.get('/products/5/detail/')
        self.assertEqual(response.status_code, 200)

    def test_detail_url_by_name(self):
        response = self.client.get(reverse('detail', kwargs={'product_id': 5}))
        self.assertEqual(response.status_code, 200)

    def test_bad_detail_url_returns_404(self):
        response = self.client.get(reverse('detail', kwargs={'product_id': 100}))
        self.assertEqual(response.status_code, 404)

    def test_detail_url_uses_correct_template(self):
        response = self.client.get(reverse('detail', kwargs={'product_id': 5}))
        self.assertTemplateUsed(response, 'products/detail.html')

    def test_detail_url_returns_good_product(self):
        response = self.client.get(reverse('detail', kwargs={'product_id': 5}))
        product = response.context['product']
        self.assertEqual(product.name, 'Product 3')
        self.assertEqual(product.brand, 'Brand 3')
        self.assertEqual(product.score, 'B')
        self.assertEqual(product.description, 'Product Description')
        self.assertEqual(product.url_img_nutrition, 'https://www.openfoodfacts.com/category/product/url_img_nutrition 3')
        self.assertEqual(product.barcode, '12345678910 3')
        self.assertEqual(product.url_off, 'https://www.openfoodfacts.com/category/product/url_off 3')


class LogonPageTestCase(TestCase):

    def test_logon_url_exists_at_location(self):
        response = self.client.get('/users/signup/')
        self.assertEqual(response.status_code, 200)

    def test_logon_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_logon_url_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_logon_post_success(self):
        response = self.client.post(reverse('signup'),
                                    data={
                                        'username': 'test_user',
                                        'first_name': 'test',
                                        'last_name': 'user',
                                        'email': 'test.user@oc.fr',
                                        'password1': 'Apass_0404',
                                        'password2': 'Apass_0404',
                                        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
    
    def test_logon_post_failure(self):
        response = self.client.post(reverse('signup'),
                                    data={
                                        'username': 'test_user2',
                                        'first_name': 'test2',
                                        'last_name': 'user2',
                                        'email': 'test2.user2@oc.fr',
                                        'password1': 'Apass_0404',
                                        'password2': 'Apss_0404',
                                        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())


class LoginPageTestCase(TestCase):

    def test_login_url_exists_at_location(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_url_uses_correct_template(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'registration/login.html')


class AccountPageTestCase(TestCase):

    def test_account_url_exists_at_location(self):
        response = self.client.get('/users/signup/')
        self.assertEqual(response.status_code, 200)

    def test_account_url_by_name(self):
        response = self.client.get(reverse('user_account'))
        self.assertEqual(response.status_code, 200)

    def test_account_url_uses_correct_template(self):
        response = self.client.get(reverse('user_account'))
        self.assertTemplateUsed(response, 'users/user_account.html')


class FavoritePageTestCase(TestCase):

    def setUp(self):
        user = self.client.post(reverse('signup'),
                               data={
                                    'username': 'test_user3',
                                    'first_name': 'test3',
                                    'last_name': 'user3',
                                    'email': 'test.user3@oc.fr',
                                    'password1': 'Apass_0404',
                                    'password2': 'Apass_0404',
                                    })

    def test_favorite_url_exists_at_location(self):
        response = self.client.get('/users/favorites/')
        self.assertEqual(response.status_code, 200)

    def test_favorite_url_by_name(self):
        response = self.client.get(reverse('user_account'))
        self.assertEqual(response.status_code, 200)

    def test_favorite_url_uses_correct_template(self):
        response = self.client.get(reverse('favorites'))
        self.assertTemplateUsed(response, 'favorites/favorites.html')

    def test_favorite_url_pagination_is_true(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('paginate' in response.context)
        self.assertTrue(response.context['paginate'] is True)

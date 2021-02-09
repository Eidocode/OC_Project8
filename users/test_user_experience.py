from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from products.models import Category, Product, Favorite


class TestUserExperience(TestCase):
    def setUp(self):
        
        category = Category(
            name='Category1',
            json_id='fr:category1',
            url='https://www.openfoodfacts.com/category1',
        )
        category.save()

        number_of_products = 40
        for pnum in range(number_of_products):
            product = Product(
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
            product.save()
            product.categories.add(category.id)

    def test_user_path(self):
        logon = self.client.post(reverse('signup'),
                               data={
                                    'username': 'test_user4',
                                    'first_name': 'test4',
                                    'last_name': 'user4',
                                    'email': 'test.user4@oc.fr',
                                    'password1': 'Apass_0404',
                                    'password2': 'Apass_0404',
                                    })
        
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        self.assertRedirects(logon, '/')

        account_page = self.client.get(reverse('user_account'))
        current_user = account_page.wsgi_request.user
        self.assertEqual(account_page.status_code, 200)
        self.assertEqual(current_user.email, 'test.user4@oc.fr')
        self.assertEqual(current_user.username, 'test_user4')
        self.assertEqual(current_user.first_name, 'test4')
        self.assertEqual(current_user.last_name, 'user4')

        categories = Category.objects.all()
        self.assertEqual(len(categories), 1)

        products = Product.objects.all()
        self.assertEqual(len(products), 40)

        search = self.client.get(reverse('search')+'?search=Product')
        self.assertEqual(search.status_code, 200)
        self.assertTrue(search.context['paginate'] is True)

        product_id = 35
        result = self.client.get(reverse('result', kwargs={'product_id': product_id}))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.context['substitutes']), 6)

        substitute = result.context['substitutes'][1]
        add_fav = self.client.get(reverse('add_fav', kwargs={'product_id': substitute.id}), HTTP_REFERER=reverse('result', kwargs={'product_id': product_id}))
        self.assertEqual(len(Favorite.objects.all()), 1)

        favorite_page = self.client.get(reverse('favorites'))
        favorites = favorite_page.context['favorites']
        self.assertEqual(len(favorites), 1)
        favorite_id = None
        for fav in favorites:
            favorite_id = fav.id
            self.assertEqual(fav.products.id, substitute.id)
        
        detail_page = self.client.get(reverse('detail', kwargs={'product_id': substitute.id}))
        self.assertEqual(detail_page.status_code, 200)
        self.assertEqual(detail_page.context['product'].name, substitute.name)
        self.assertEqual(detail_page.context['product'].score, substitute.score)
        self.assertEqual(detail_page.context['product'].barcode, substitute.barcode)
        self.assertEqual(detail_page.context['product'].description, substitute.description)
        self.assertEqual(detail_page.context['product'].url_off, substitute.url_off)
        self.assertEqual(detail_page.context['product'].url_img_nutrition, substitute.url_img_nutrition)

        del_favorite = self.client.get(reverse('del_fav', kwargs={'favorite_id': favorite_id}), HTTP_REFERER=reverse('favorites'))
        self.assertEqual(del_favorite.status_code, 302)
        self.assertRedirects(del_favorite, '/users/favorites/')
        favorites = Favorite.objects.all()
        self.assertEqual(len(favorites), 0)

        logout = self.client.get('/logout/')
        self.assertEqual(logout.status_code, 302)
        self.assertRedirects(logout, '/')

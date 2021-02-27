import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from django.urls import reverse

from products.models import Category, Product, Favorite


class TestAppIntegration(StaticLiveServerTestCase):
    """
        integration tests of purbeurre app
    """

    def setUp(self):
        time.sleep(1)
        # Initialize driver for chrome
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        # Logon new user
        self.logon_user = self.client.post(
                    reverse('signup'),
                    data={
                        'username': 'test_user5',
                        'first_name': 'test5',
                        'last_name': 'user5',
                        'email': 'test.user5@oc.fr',
                        'password1': 'Apass_0404',
                        'password2': 'Apass_0404',
                    })

    def tearDown(self):
        time.sleep(1)
        self.driver.quit()

    def test_homepage(self):
        # Opens homepage & checks the title
        self.driver.get(self.live_server_url)
        self.assertTrue(self.driver.title == "Pur Beurre App'")

    def test_logon_new_user(self):
        # Tests logon user from signup page

        # New user informations
        user = {
            'username': "toto",
            'fname': "Toto",
            'lname': "Tutu",
            'email': "Toto.Tutu@oc.fr",
            'password': "motdepasse123",
        }

        self.driver.get(self.live_server_url+'/users/signup/')

        # username
        username_field = self.driver.find_element_by_id("id_username")
        username_field.send_keys(user['username'])

        # First name
        fname_field = self.driver.find_element_by_id("id_first_name")
        fname_field.send_keys(user['fname'])

        # last name
        lname_field = self.driver.find_element_by_id("id_last_name")
        lname_field.send_keys(user['lname'])

        # email
        email_field = self.driver.find_element_by_id("id_email")
        email_field.send_keys(user['email'])

        # password
        pass1_field = self.driver.find_element_by_id("id_password1")
        pass1_field.send_keys(user['password'])

        # confirme password
        pass2_field = self.driver.find_element_by_id("id_password2")
        pass2_field.send_keys(user['password'])

        # submit informations
        time.sleep(1)
        submit = self.driver.find_element_by_id('logon_btn')
        submit.send_keys(Keys.RETURN)

        # Checks objects in User table
        users = User.objects.all()
        self.assertEqual(len(users), 2)  # must returns 2
        # Logon successful redirection
        self.assertEqual(self.driver.current_url, self.live_server_url+'/')

    def login(self):
        # Method for login user

        self.driver.get(self.live_server_url + '/login/')

        # username
        username_field = self.driver.find_element_by_id("id_username")
        username_field.send_keys("test_user5")

        # password
        username_field = self.driver.find_element_by_id("id_password")
        username_field.send_keys("Apass_0404")

        # submit login informations
        time.sleep(1)
        submit = self.driver.find_element_by_id('login_btn')
        submit.send_keys(Keys.RETURN)

    def test_login_user(self):
        # Tests login user from signin page

        # Uses login method
        self.login()
        # Checks login successful redirection
        self.assertEqual(self.driver.current_url, self.live_server_url+'/')

        # Checks that search button is enabled (only when a user is logged in)
        time.sleep(1)
        btn = self.driver.find_element_by_id("send_btn")
        self.assertTrue(btn.is_enabled())

    def add_to_db(self):
        # Method used to add new items to database

        # Adds 1 category in test database
        category = Category(
            name='Category2',
            json_id='fr:category2',
            url='https://www.openfoodfacts.com/category2',
        )
        category.save()

        # Add a product in test database
        number_of_products = 1
        for pnum in range(number_of_products):
            num = 100 + pnum
            product = Product(
                name=f'Product {num}',
                brand=f'Brand {num}',
                description='Product Description',
                score='B',
                barcode=f'12345678910 {num}',
                url_img_small=f'https://www.off.com/cat/prod/img_small{num}',
                url_img=f'https://www.off.com/cat/prod/img{num}',
                url_off=f'https://www.off.com/cat/prod/off{num}',
                url_img_nutrition=f'https://www.off.com/cat/prod/img_nt{num}',
            )
            product.save()
            product.categories.add(category.id)

    def test_search_product_and_favorites(self):
        # Tests search product, search page, result page and favorites

        # Login a user & add elements to database
        self.login()
        self.add_to_db()

        # search a product
        search_field = self.driver.find_element_by_id('id_search')
        search_field.send_keys("Product")
        time.sleep(1)
        submit = self.driver.find_element_by_id('send_btn')
        submit.send_keys(Keys.RETURN)  # Submit research
        # Checks products in db & result page
        products = Product.objects.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(
            self.driver.current_url,
            self.live_server_url+'/products/search/?search=Product'
        )

        # Test product result page
        p_url = '/products/' + str(products[0].id) + '/'
        time.sleep(1)
        self.driver.get(self.live_server_url + p_url)
        # Click on first save button (favorite)
        save = self.driver.find_element_by_id("save1")
        save.send_keys(Keys.RETURN)

        # Test favorites result page
        self.driver.get(self.live_server_url + '/users/favorites/')
        time.sleep(1)
        # Checks favorites in database (must return 1)
        favorites = Favorite.objects.all()
        self.assertEqual(len(favorites), 1)
        # Click on first remove button (favorite)
        del_elem = self.driver.find_element_by_id("delete1")
        del_elem.send_keys(Keys.RETURN)
        # Checks favorites in database (must return 2)
        favorites = Favorite.objects.all()
        self.assertEqual(len(favorites), 0)

    def test_logout_user(self):
        # Tests logout user

        # Login user
        self.login()

        # identifies disconnect icon
        self.driver.find_element_by_xpath('//*[@title="Déconnexion"]').click()
        time.sleep(1)

        # Checks that search button is disabled (only when no user's logged in)
        btn = self.driver.find_element_by_id("send_btn")
        self.assertFalse(btn.is_enabled())

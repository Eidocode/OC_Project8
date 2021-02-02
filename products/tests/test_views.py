from django.test import TestCase
from django.urls import reverse

class IndexPageTestCase(TestCase):
    # Test that index page returns 200
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    # Test that a research returns 200
    def test_search_product(self):
        response = self.client.get(reverse('search')+'?query=test')
        self.assertEqual(response.status_code, 200)
    
    # Test that a bad research returns 404
    def test_search_product(self):
        response = self.client.get(reverse('search')+'query=test')
        self.assertEqual(response.status_code, 404)
    
    # Test that result page returns 404 with an unexisting product
    def test_bad_search_product(self):
        response = self.client.get(reverse('result', args=('5')))
        self.assertEqual(response.status_code, 404)

    def test_result_product(self):
        pass

    def test_detail_product(self):
        pass

    def test_favorite_product(self):
        pass

    def test_registration_user(self):
        pass

    def test_login_user(self):
        pass
    
    def test_logoff_user(self):
        pass
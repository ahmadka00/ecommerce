from importlib import import_module
from unittest import skip

from django.conf import settings 
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
# from django.test import RequestFactory

from store.views import products_all
from store.models import Category, Product

# @skip("demonstrating skipping")
# class TestSkip(TestCase):
#     def test_skip_example(self):
#         pass

class TestViewResponses(TestCase):
        def setUp(self):
            self.c = Client()
            User.objects.create(username='admin')
            Category.objects.create(name='django', slug='django')
            Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                                            slug='django-beginners', price='20.00', image='django')
    

        def test_url_allowed_hosts(self):
             """
             Test allowed hosts
             """
             response = self.c.get('/')
             self.assertEqual(response.status_code, 200)

        def test_product_detail_url(self):
            """
            Test Product response status
            """
            response = self.c.get(reverse('store:product_detail', args=['django-beginners']))
            self.assertEqual(response.status_code, 200)

        def test_Category_detail_url(self):
            """
            Test Category response status
            """
            response = self.c.get(reverse('store:category_list', args=['django']))
            self.assertEqual(response.status_code, 200)
        
        def test_homepage_html(self):
            """
            Example: code validation, search HTML for text
            """
            request = HttpRequest()
            engine = import_module(settings.SESSION_ENGINE)
            request.session = engine.SessionStore()
            response = products_all(request)
            html = response.content.decode('utf8')
            self.assertIn('<title> Home </title>', html)
            self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
            self.assertEqual(response.status_code, 200)


        # def  test_view_function(self):
        #     request = self.factory.get('/item/django-beginners')
        #     response = all_products(request)
        #     html = response.content.decode('utf8')
        #     self.assertIn('<title> Home </title>', html)
        #     self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        #     self.assertEqual(response.status_code, 200)

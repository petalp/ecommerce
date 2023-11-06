from django.test import TestCase
from django.contrib.auth.models import User
from store.models import Category, Product
from django.urls import reverse
from django.test import Client,RequestFactory,TestCase
from store.views import product_all
from django.http import HttpRequest
from unittest import skip

@skip("demonstrating skipping")
class TestSkip(TestCase):
    def test_skip_example(self):
        pass

class TestViewResponse(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        User.objects.create(username='admin')
        Category.objects.create(name='computer science', slug='computer science')
        Product.objects.create(category_id=1, title='computer science', created_by_id=1,
                                slug='computer science', price='20.00',image='computer science')
    
    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)


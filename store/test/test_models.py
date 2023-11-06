from django.test import TestCase
from django.contrib.auth.models import User

from store.models  import Category, Product

class TestCategoriesModel(TestCase):

    def setUp(self) -> None:
        self.data1 = Category.objects.create(name='computer_science', slug='computer_science')
    
    def test_category_model_entry(self):
        """
        Test Category model data insertion/types attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types attributes
        """
        data = self.data1
        self.assertEqual(str(data), 'computer_science')


class TestProductModel(TestCase):
    def setUp(self) -> None:
        Category.objects.create(name='computer_science', slug='computer_science')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1,title='computer_science',created_by_id=1,
                                            slug='computer_science', price='20.20', image='cs')
    def test_product_model_entry(self):
        """
        Test Category model data insertion/types attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'computer_science')

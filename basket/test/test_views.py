from django.contrib.auth.models import User 
from django.test import TestCase
from django.urls import reverse


from store.models import Product, Category


class TestBasketView(TestCase):
    def setUp(self) -> None:
        User.objects.create(username='admin')
        Category.objects.create(name='computer science', slug='computer science')
        
        Product.objects.create(category_id=1, title='backend development', created_id=1,
                                slug='backend development', price='20.00', image='backend development')
        
        
        Product.objects.create(category_id=1, title='backend development', created_id=1,
                                slug='backend development', price='20.00', image='backend development')
        
        Product.objects.create(category_id=1, title='backend development', created_id=1,
                                slug='backend development', price='20.00', image='backend development')
        

        self.client.post(
            reverse('basket:basket_add'), {'productid':1, 'productqty':1, 'action':'post'}, xhr=True
        )

        self.client.post(
            reverse('basket:basket_add'),{'productid':2, 'productqty':2, "action":"post"}, xhr=True
        )


    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Test adding items to the basket 
        """
        response = self.client.post(
            reverse('basket:basket_add'), {'productid':3, 'productqty':1, 'action':'post'}, xhr=True
        )
        self.assertEqual(response.json(), {'qty':3})

    def test_basket(self):
        """
        Test adding items to the basket
        """
        response = self.client.post(
            reverse('basket:basket_add'), {'productid':3,'prodctqty':1, 'action':'post'}, xhr=True
        )
        self.assertEqual(response.json(), {'qty':3})


    def test_basket_delete(self):
        """
        Test deleting items from the basket
        """
        response = self.client.post(
            reverse('basket:basket_delete'), {'productid':2, 'action':'post'}, xhr=True
        )
        self.assertEqual(response.json(), {'qty':1, 'subtotal':'20.0'})

    def test_basket_update(self):
        """
        Test updating items from the basket
        """
        response = self.client.post(
            reverse('basket:basket_update'), {'productqty':1, 'action':'post'}, xhr=True
        )
        self.assertEqual(response.json(), {'qty':2, 'subtotal':'40.0'})
        

from django.db import models
from django.conf import settings
from django.db.models.query import QuerySet
from django.urls import reverse

# Create your models here.
class ProductManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super(ProductManager, self).get_queryset().filter(is_active=True)

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
    
    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])
    
    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default="admin")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/',default='images/default.jpeg')
    slug = models.SlugField(max_length=200)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()


    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self) -> str:
        return self.title



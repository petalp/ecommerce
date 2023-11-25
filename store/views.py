from django.shortcuts import render, get_object_or_404
from .models import Category, Product

# Create your views here.

def product_all(request):
    product = Product.products.all()
    context = {'products':product}
    return render(request, 'store/home.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    context = {'product':product}
    return render(request, 'store/single.html', context)

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = Product.objects.filter(category=category)
    context = {'category':category, 'products':product}
    return render(request, 'store/category.html', context)
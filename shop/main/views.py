from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
    categories = Category.objects.all() # вывод всех объектов
    products = Product.objects.filter(available = True) # вывод объектов соотв фильтрации
    
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
        
    return render(
    request,
    "main/product/list.html",
    {
        "category": category,
        "categories": categories,
        "products": products,
    }
)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    # exclude = возвращает новый набор объектов из БД, исключая из выборки те , которые соот параметрам поиска
    related_products = Product.objects.filter(category=product.category,
                                              available=True).exclude(id=product.id)[:4]
    
    cart_product_form = CartAddProductForm()
    
    return render(
        request,
        'main/product/detail.html',
        {
            'product':product,
            'related_products':related_products,
            'cart_product_form' : cart_product_form, 
        }
    )
    
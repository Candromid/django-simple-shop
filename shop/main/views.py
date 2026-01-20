from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

from django.db.models.functions import Lower  # для сортировки строк без учёта регистра

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()  # все категории для меню
    products = Product.objects.filter(available=True)  # базовый список доступных товаров

    if category_slug:
        # если категория указана в URL — фильтруем товары
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    sort = request.GET.get('sort')  # параметр сортировки из строки запроса

    if sort == 'name':
        # сортировка по названию (А–Я), без учёта регистра
        products = products.order_by(Lower('name'))
    elif sort == '-name':
        # сортировка по названию (Я–А), без учёта регистра
        products = products.order_by(Lower('name').desc())
    elif sort == 'price':
        # сортировка по цене (дешёвые → дорогие)
        products = products.order_by('price')
    elif sort == '-price':
        # сортировка по цене (дорогие → дешёвые)
        products = products.order_by('-price')
    else:
        # сортировка по умолчанию
        products = products.order_by('name')

    return render(request, 'main/product/list.html', {
        'category': category,       # текущая категория
        'categories': categories,   # список всех категорий
        'products': products,       # отсортированные товары
    })


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
    
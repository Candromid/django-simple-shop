from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)  # создаём / получаем корзину из сессии
    product = get_object_or_404(Product, id=product_id)  # получаем товар или 404
    form = CartAddProductForm(request.POST)  # форма добавления товара

    if form.is_valid():
        cd = form.cleaned_data  # очищенные данные формы
        cart.add(
            product=product,
            quantity=cd['quantity'],           # сколько добавить
            override_quantity=cd['override']   # заменить или прибавить
        )
    return redirect('cart:cart_detail')  # редирект на страницу корзины

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request) # инициализация корзины
    product = get_object_or_404(Product, id=product_id) # получаем товар 
    cart.remove(product) # удаляем товар
    
    return redirect('cart:cart_detail') # возвращаемся в корзину

def cart_detail(request):
    cart = Cart(request)  # получаем корзину

    for item in cart:
        # форма обновления количества для каждого товара
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],  # текущее количество
            'override': True,              # при сабмите заменяем количество
        })

    return render(request, 'cart/detail.html', {
        'cart': cart  # передаём корзину в шаблон
    })

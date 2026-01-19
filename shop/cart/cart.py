from django.conf import settings
from main.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session  # берём сессию текущего пользователя

        cart = self.session.get(settings.CART_SESSION_ID)  # пытаемся получить корзину из сессии
        if not cart:
            # если корзины нет — создаём пустую и сохраняем в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart  # сохраняем корзину в объекте для удобной работы

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)  # id товара используем как ключ (сессия хранит только строки)

        if product_id not in self.cart:
            # если товара ещё нет в корзине — создаём запись
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),  # цена строкой для корректной сериализации
            }

        if override_quantity:
            # заменяет количество на указанное число (юзером)
            self.cart[product_id]['quantity'] = quantity
        else:
            # увеличить количество (обычное добавление)
            self.cart[product_id]['quantity'] += quantity

        self.save()  # сохраняем изменения в сессии
        
    def save(self): 
        self.session.modified = True  # пересохраняет текущую сессию на измененную 
        
    def remove(self, product): # удаление продукта из корзины
        product_id = str(product.id)
        
        if product_id in self.cart:  
            del self.cart[product_id] 
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()  # получаем id всех товаров в корзине

        products = Product.objects.filter(id__in=product_ids)  # одним запросом загружаем товары из БД
        cart = self.cart.copy()  # копия корзины, чтобы не менять данные в сессии

        for product in products:
            # добавляем объект Product к соответствующему элементу корзины
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = float(item['price'])  # цена 1 товара (одной позиции)
            item['total_price'] = item['price'] * item['quantity']  # цена за все товары одной позиции
            yield item  # делаем корзину итерируемой
            
    def __len__(self):
        # возвращает количество товаров в корзине и отображает над иконкой корзины
        return sum(item['quantity'] for item in self.cart.values())  
    
    def get_total_price(self):
        # возвращает общую сумму всех товаров в корзине
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]  # очистка корзины  (очистка cookies связанные только с корзиной )
        self.save()
from decimal import Decimal

from django.conf import settings

from epharmacyweb.models import Product

class Cart():

    # Creates a cart session ID
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # To add item(s) to the cart
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price':str(product.price)}
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    # To delete items from the cart
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.products.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['subtotal'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # Calculates the subtotal
    def get_subtotal(self):
        return sum(Decimal(item['price']) * int(item['quantity']) for item in self.cart.values())

    # Calculates the tax
    def get_tax(self):
        tax = Decimal('0.10')
        tax_price = sum(Decimal(item['price']) * int(item['quantity']) for item in self.cart.values()) * Decimal(tax)
        return tax_price

    # Calculates the grand total
    def get_total(self):
        
        subtotal = sum(Decimal(item['price']) * int(item['quantity']) for item in self.cart.values())
        tax = Decimal('0.10')
        tax_price = sum(Decimal(item['price']) * int(item['quantity']) for item in self.cart.values()) * Decimal(tax)

        shipping_cost = 5
        total = Decimal(subtotal) + Decimal(tax_price) + Decimal(shipping_cost)
        return total
        
    # Empties the cart
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
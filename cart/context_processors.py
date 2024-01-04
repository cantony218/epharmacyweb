from .cart import Cart

# Retrieves the cart file
def cart(request):
    return {'cart': Cart(request)}
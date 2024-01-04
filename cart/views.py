from django.shortcuts import render, redirect, get_object_or_404
from epharmacyweb.models import Product
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_summary')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_summary')

# Retrieves the cart page only when the user is logged in.
@login_required
def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/summary.html', {'cart':cart})
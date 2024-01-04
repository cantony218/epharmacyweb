import stripe
from django.shortcuts import render, get_object_or_404

from .models import Category, Product, Contact
from cart.forms import CartAddProductForm

stripe.api_key = 'sk_test_51KHfkzEeX9bmWjgu3gYM9xx50dvPIbkrUJq697PEhJQgR4q2zM3IM5feYxzeGKHDtUoQA733S5vJSosjMO7kwTeR00LKx47TQe'

# Displays all products
def all_products(request):
    products = Product.products.all()
    return render(request, 'epharmacyweb/index.html', {'products': products})

# Displays the product page
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'epharmacyweb/detail.html', {'product': product, 'cart_product_form': cart_product_form})

# Displays all the categories
def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'epharmacyweb/category.html', {'category': category, 'products': products})

# Displays the privacy policy page
def privacy(request):
    return render(request, 'epharmacyweb/privacy.html')

# Displays the terms and conditions page
def terms(request):
    return render(request, 'epharmacyweb/terms.html')

# Displays the Search page
def search(request):
    searched = request.GET.get('searched')
    products = Product.objects.filter(title__icontains=searched)
    
    if products:
        return render(request, 'epharmacyweb/search.html', {'searched': searched, 'products': products})
    else:
        return render(request, 'epharmacyweb/search_error.html')

def search_error(request):
    return render(request, 'epharmacyweb/search_error.html')

def contact_form(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact.name = name
        contact.email = email
        contact.subject = subject
        contact.message = message
        contact.save()
        return render(request, 'epharmacyweb/contact_us_sent.html')
    return render(request, 'epharmacyweb/contact_us.html')
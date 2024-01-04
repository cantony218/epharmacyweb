from django.urls import path, include

from . import views

app_name = 'epharmacyweb'

urlpatterns = [
    path('cart-summary/', include('cart.urls', namespace='cart_summary')),
    path('', views.all_products, name='pharmacy_home'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('search/', views.search, name='search'),
    path('search_error/', views.search_error, name='search_error'),
    path('contact_us/', views.contact_form, name='contact_us'),
]
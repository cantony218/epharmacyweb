from django.contrib import admin

from .models import Order, OrderItem

# Displays the orders and ordered items on the admin page.
admin.site.register(Order)
admin.site.register(OrderItem)
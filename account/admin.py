from django.contrib import admin
from .models import UserBase

# Connects the UserBase model to the Admin page.
admin.site.register(UserBase)
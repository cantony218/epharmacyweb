from .models import Category

# Makes the category appear multiple in the admin page.
def categories(request):
    return {
        'categories': Category.objects.all()
    }
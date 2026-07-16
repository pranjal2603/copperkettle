from .models import MenuCategory


def menu_categories(request):
    return {'nav_categories': MenuCategory.objects.all()}
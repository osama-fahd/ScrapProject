from django.contrib import admin
from .models import Category, Part, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Part)
admin.site.register(Product)
from django.shortcuts import render
from accounts.models import ProfileSeller
from autoparts.models import Product, Part
from Vehicle.models import Brand , Car

# Create your views here.

def seller_dashboard(request):
    return render(request, 'sellers/seller_dashboard.html')

def seller_products(request):

    return render(request, 'sellers/manage_product.html')

def seller_add_product(request):
    cars = Car.objects.all()
    parts = Part.objects.all()
    
    return render(request, 'sellers/seller_add_product.html', {'part_directions': Product.PartDirection.choices, "cars": cars, "part": parts })

def seller_stock(request):
    return render(request, 'sellers/seller_inventory.html')

# def seller_edit_product(request, product_id):
#     return render(request, 'sellers/edit_product.html')

# def seller_delete_product(request, product_id):
#     return render(request, 'sellers/delete_product.html')

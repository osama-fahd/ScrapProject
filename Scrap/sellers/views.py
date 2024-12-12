from django.shortcuts import render

# Create your views here.

def seller_dashboard(request):
    return render(request, 'sellers/seller_dashboard.html')

def seller_products(request):

    return render(request, 'sellers/manage_product.html')

def seller_add_product(request):
    return render(request, 'sellers/seller_add_product.html')

def seller_stock(request):
    return render(request, 'sellers/seller_inventory.html')

# def seller_edit_product(request, product_id):
#     return render(request, 'sellers/edit_product.html')

# def seller_delete_product(request, product_id):
#     return render(request, 'sellers/delete_product.html')

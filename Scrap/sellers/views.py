from django.shortcuts import render
from accounts.models import ProfileSeller
from autoparts.models import Product, Part
from Vehicle.models import Brand , Car
# from sellers.forms import ProductForm

# Create your views here.

def seller_dashboard(request):
    return render(request, 'sellers/seller_dashboard.html')

def seller_products(request):

    return render(request, 'sellers/manage_product.html')

def seller_add_product(request):
    cars = Car.objects.all()
    parts = Part.objects.all()
    profile_seller = ProfileSeller.objects.get(user=request.user)
    if request.method == 'POST':
        part_id = request.POST.get('part')
        car_id = request.POST.get('car') 
        part_direction = request.POST.get('part_direction')
        stock = request.POST.get('stock')
        condition = request.POST.get('condition')
        made = request.POST.get('made')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('logo')

        product = Product(
            part_id=part_id,
            seller=profile_seller,
            part_direction=part_direction,
            made=made,
            stock=stock,
            condition=condition,
            start_date=start_date,
            end_date=end_date,
            price=price,
            description=description,
            image=image
        )
        product.save()

        if car_id:
            car_obj = Car.objects.get(id=car_id)
            product.car.add(car_obj)

    return render(request, 'sellers/seller_add_product.html', {'part_directions': Product.PartDirection.choices, "cars": cars, "part": parts })

def seller_stock(request):
    return render(request, 'sellers/seller_inventory.html')

# def seller_edit_product(request, product_id):
#     return render(request, 'sellers/edit_product.html')

# def seller_delete_product(request, product_id):
#     return render(request, 'sellers/delete_product.html')

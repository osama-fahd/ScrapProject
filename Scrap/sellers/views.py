from django.shortcuts import render,redirect
from accounts.models import ProfileSeller
from autoparts.models import Product, Part ,Category
from Vehicle.models import Brand , Car
from sellers.forms import ProductForm
from django.contrib import messages
from django.http import HttpRequest


# Create your views here.

def seller_dashboard(request):
    products = Product.objects.all()
    return render(request, 'sellers/seller_dashboard.html',{"product":products})

def seller_products(request):

    return render(request, 'sellers/manage_product.html')
def seller_add_product(request: HttpRequest):
    try:
        seller = request.user.profileseller
    except ProfileSeller.DoesNotExist:
        messages.error(request, "No seller profile found for this user.")
        return redirect("main:home_view")

    cars = Car.objects.all()
    parts = Part.objects.all()
    categories = Category.objects.all()

    if request.method == "POST":
        part_id = request.POST.get('part')
        car_ids = request.POST.getlist('car') 
        part_direction = request.POST.get('part_direction')
        made = request.POST.get('made')
        stock = request.POST.get('stock')
        condition = request.POST.get('condition')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        try:
            # Retrieve the Part object
            part = Part.objects.get(id=part_id)

            # Create and save the product
            product = Product(
                part=part,
                seller=seller,
                part_direction=part_direction,
                made=made,
                stock=stock,
                condition=condition,
                start_date=start_date,
                end_date=end_date,
                price=price,
                description=description,
                image=image,
            )
            product.save()

            # Add related cars if provided
            for car_id in car_ids:
                car_obj = Car.objects.get(id=car_id)
                product.car.add(car_obj)

            messages.success(request, "تمت اضافة خردتك")
            return redirect("autoparts:all_parts_view")
        except Part.DoesNotExist:
            messages.error(request, "اكمل جميع الحقول")
        except Exception as e:
            messages.error(request, f"حصلت مشكلة{e}")

    return render(
        request,
        "sellers/seller_add_product.html",
        {
            "cars": cars,
            "parts": parts,
            "categories": categories,
            "part_directions": Product.PartDirection.choices,
        }
    )




def seller_stock(request):
    return render(request, 'sellers/seller_inventory.html')

# def seller_edit_product(request, product_id):
#     return render(request, 'sellers/edit_product.html')

# def seller_delete_product(request, product_id):
#     return render(request, 'sellers/delete_product.html')

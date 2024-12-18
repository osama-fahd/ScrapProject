from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from .forms import BrandForm, CarForm
from .models import Brand,Car
from django.db import transaction

# Create your views here.

def new_brand(request: HttpRequest):

    if request.method == "POST":
        brand_form = BrandForm(request.POST, request.FILES)  
        if brand_form.is_valid():
            brand_form.save()  
            messages.success(request, "تم اضافة الماركة بنجاح", "alert-success")
            return redirect('main:home_view')  
        else:
            messages.error(request, "لا يمكن اضافة الماركة", "alert-danger")
    else:
        brand_form = BrandForm()

    return render(request, "Vehicle/new_brand.html")

def new_car(request: HttpRequest):
    brands = Brand.objects.all()
    if request.method == "POST":
        car_form = CarForm(request.POST, request.FILES)
        if car_form.is_valid():
            car_form.save()
            messages.success(request, "تم اضافة السيارة بنجاح", "alert-success")
            return redirect('main:home_view')  
        else:
            messages.error(request, "خطأ عدم امكانية اضافة السيارة", "alert-danger")
    else:
        car_form = CarForm()

    return render(request, "Vehicle/new_car.html", {'brands':brands})












@transaction.atomic
def save_brands_to_database(request: HttpRequest):
    # First delete all existing categories and parts
    Car.objects.all().delete()  # Delete parts first because they reference categories
    Brand.objects.all().delete()
    
    # Reset the SQLite sequence
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='Vehicle_brand';")

    # Add categorizes to the database
    brands = [
        {"name": "تويوتا", "name_en": "Toyota" , "logo": "brand_logos/toyota.jpg"},
        {"name": "فورد", "name_en": "Ford", "logo": "brand_logos/ford.png"},
        {"name": "هونداي", "name_en": "Hyundai", "logo": "brand_logos/Hyundai.png"},
        {"name": "مازدا", "name_en": "Mazda", "logo": "brand_logos/mazda.png"},
       
    ]

    for item in brands:
        brand_object = Brand(name=item["name"], name_en=item["name_en"],logo=item["logo"] )
        brand_object.save()

    return redirect("main:home_view")


@transaction.atomic
def save_cars_to_database(request: HttpRequest):
    # Add cars to the database
    cars_data = [
        {"car_brand_id": 1, "name": "كامري"},
        {"car_brand_id": 1, "name": "أفالون"},
        {"car_brand_id": 2, "name": "تورس"},
        {"car_brand_id": 2, "name": "F-150"},
        {"car_brand_id": 3, "name": "ألنترا"},
        {"car_brand_id": 3, "name": "سوناتا"},
        {"car_brand_id": 4, "name": "مازدا-6"},
        {"car_brand_id": 4, "name": "مازدا-CX9"},
        ]

    for item in cars_data:
        brand_object = Brand.objects.get(pk=item["car_brand_id"])
        car_object = Car(brand=brand_object, name=item["name"])
        car_object.save()
    
    return redirect("main:home_view")
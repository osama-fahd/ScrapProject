from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from .forms import BrandForm, CarForm
from .models import Brand,Car
# Create your views here.

def new_brand(request: HttpRequest):

    if request.method == "POST":
        brand_form = BrandForm(request.POST, request.FILES)  
        if brand_form.is_valid():
            brand_form.save()  
            messages.success(request, "Brand added successfully!")
            return redirect('main:home_view')  
        else:
            messages.error(request, "brand can't be added")
    else:
        brand_form = BrandForm()

    return render(request, "Vehicle/new_brand.html")

def new_car(request: HttpRequest):
    brands = Brand.objects.all()
    if request.method == "POST":
        car_form = CarForm(request.POST, request.FILES)
        if car_form.is_valid():
            car_form.save()
            messages.success(request, "Car added successfully!")
            return redirect('main:home_view')  
        else:
            messages.error(request, "Car can't be added")
    else:
        car_form = CarForm()

    return render(request, "Vehicle/new_car.html", {'brands':brands})
from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import ProfileSeller,ProfileCustomer,Review
from autoparts.models import Product, Part ,Category
from Vehicle.models import Brand , Car
from sellers.forms import ProductForm
from django.contrib import messages
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from customer.models import Cart



# Create your views here.

def seller_dashboard(request):
    try:
        seller = request.user.profileseller
    except ProfileSeller.DoesNotExist:
        messages.error(request, "No seller profile found for this user.")
        return redirect("main:home_view")

    # Filter data
    products = Product.objects.filter(seller=seller)
    categories = Category.objects.all()
    cars = Car.objects.all()
    brands = Part.objects.values_list('name', flat=True).distinct() 
    years = range(2000, 2025)

    # Apply filters
    auto_parts = request.GET.get('autoParts')
    year = request.GET.get('year')
    brand = request.GET.get('brand')
    car_id = request.GET.get('car')

    if auto_parts:
        products = products.filter(part__part_category__id=auto_parts)
    if year:
        products = products.filter(start_date__lte=year, end_date__gte=year)
    if brand:
        products = products.filter(part__name=brand)
    if car_id:
        products = products.filter(car__id=car_id)
        

    paginator = Paginator(products, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'cars': cars,
        'brands': brands,
        'years': years,
    }
    return render(request, 'sellers/seller_dashboard.html', context)


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


@login_required
def update_product(request, product_id):
    try:
        seller = request.user.profileseller
    except ProfileSeller.DoesNotExist:
        messages.error(request, "No seller profile found for this user.")
        return redirect("main:home_view")

    product = get_object_or_404(Product, id=product_id, seller=seller)
    categories = Category.objects.all()
    parts = Part.objects.all()
    cars = Car.objects.all()
    brands = Part.objects.values_list('name', flat=True).distinct()  # Assuming 'name' represents brand
    years = range(2000, 2025)  

    if request.method == "POST":
        category_id = request.POST.get('category')
        part_id = request.POST.get('part')
        car_ids = request.POST.getlist('car') 
        part_direction = request.POST.get('part_direction')
        stock = request.POST.get('stock')
        condition = request.POST.get('condition')
        made = request.POST.get('made')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')  

        # Validate required fields
        if not category_id or not part_id or not price or not description:
            messages.error(request, "Category, Part, price, and description are required fields.")
            return render(
                request,
                "seller/edit_product.html",
                {
                    "product": product,
                    "categories": categories,
                    "parts": parts,
                    "cars": cars,
                    "brands": brands,
                    "years": years,
                    "part_directions": Product.PartDirection.choices,
                }
            )

        try:
            category = get_object_or_404(Category, id=category_id)
            part = get_object_or_404(Part, id=part_id)

            product.part = part
            product.part_direction = part_direction
            product.stock = stock
            product.condition = condition
            product.made = made
            product.start_date = start_date
            product.end_date = end_date
            product.price = price
            product.description = description

            if image:
                product.image = image

            product.save()

            product.car.clear()
            for car_id in car_ids:
                car_obj = get_object_or_404(Car, id=car_id)
                product.car.add(car_obj)

            messages.success(request, "Product updated successfully!")
            return redirect("seller:seller_dashboard")
        except Exception as e:
            messages.error(request, f"There was an error updating the product: {e}")

    selected_cars = product.car.values_list('id', flat=True)

    return render(
        request,
        "sellers/edit_product.html",
        {
            "product": product,
            "categories": categories,
            "parts": parts,
            "cars": cars,
            "brands": brands,
            "years": years,
            "part_directions": Product.PartDirection.choices,
            "selected_cars": selected_cars,
        }
    )

def seller_profile_view(request: HttpRequest, seller_id: int):
    seller = get_object_or_404(ProfileSeller, id=seller_id)
    
    products = Product.objects.filter(seller=seller)
    
    reviews = Review.objects.filter(seller=seller)
    
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'seller': seller,
        'products': page_obj,
        'reviews': reviews,
        'average_rating': average_rating,
    }
    
    return render(request, 'sellers/sellers_profiles.html', context)

def order_item_view(request,cart_id:Cart):
    cart= Cart.objects.get(pk=cart_id)
    customer = cart.customer

    for cartitem in cart.cartitem_set.all():
        if cartitem.product.seller.id == request.user.profileseller.id():
            product=cartitem.product(

            )


        


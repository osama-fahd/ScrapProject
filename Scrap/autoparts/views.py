from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.db import transaction, models
import random
from .models import Category, Part, Product
from Vehicle.models import Car, Brand
from accounts.models import ProfileSeller
from django.core.paginator import Paginator
from django.contrib import messages
import csv
from django.conf import settings
import os

# Create your views here.
def all_parts_view(request: HttpRequest):
    categories = Category.objects.all()
    parts = Part.objects.all()
    context = {"categories": categories}

    return render(request, "autoparts/all_parts.html", context)


def products_view(request: HttpRequest, part_id):
    chosen_part = Part.objects.get(pk=part_id)
    
    # Start with all products for this part, annotated with average rating
    products = Product.objects.filter(part=chosen_part).annotate(
        avg_rating=models.Avg('seller__review__rating')
    )

    # Show no products availble for this part if there is no products
    if not products:
        messages.warning(request, "لا تتوفر منتجات معروضة حالياً ضمن القطعة المختارة، بامكانكم تصفح باقي القطع", "alert-warning")
        return redirect("main:home_view")

    
    # Get min and max years from the products
    year_range = products.aggregate(
        min_year=models.Min('start_date'),
        max_year=models.Max('end_date')
    )
    
    # Apply filters based on GET parameters
    if "search" in request.GET and request.GET["search"]:
        products = products.filter(description__contains=request.GET["search"])
        
    if "brand" in request.GET and request.GET["brand"]:
        products = products.filter(car__brand_id=request.GET["brand"])
        
    if "car" in request.GET and request.GET["car"]:
        products = products.filter(car__id=request.GET["car"])
        
    if "year" in request.GET and request.GET["year"]:
        selected_year = int(request.GET["year"])
        products = products.filter(
            start_date__lte=selected_year,
            end_date__gte=selected_year
        )
    
    # Get unique cars and brands for these filtered products
    cars = Car.objects.filter(products__in=products).distinct()
    brands = Brand.objects.filter(car__in=cars).distinct()
    
    # Generate list of years for the dropdown
    years = range(year_range['min_year'], year_range['max_year'] + 1)

    # Add select_related for seller to optimize queries
    products = products.select_related('seller')
    
    # Pagination
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        "chosen_part": chosen_part,
        "products": page_obj,
        "brands": brands,
        "cars": cars,
        "years": years,
        "selected_year": request.GET.get("year", ""),
        "page_obj": page_obj,
    }

    return render(request, "autoparts/products.html", context)





# save to the database
@transaction.atomic
def save_categories_to_database(request: HttpRequest):
    # First delete all existing categories and parts
    Part.objects.all().delete()  # Delete parts first because they reference categories
    Category.objects.all().delete()
    
    # Reset the SQLite sequence
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='autoparts_category';")

    # Add categorizes to the database
    categories = [
        {"name": "المحركات والقير", "name_en": "Engine & Transmission"},
        {"name": "قطع كهربائية", "name_en": "Electrical"},
        {"name": "البودي", "name_en": "Exterior & Body"},
        {"name": "الأنوار", "name_en": "Lights"},
        {"name": "التبريد والتكييف", "name_en": "Cooling & Heating"},
        {"name": "الداخلية والاكسسوارت", "name_en": "Interior & Accessories"},
        {"name": "الميزانية / نظام التعليق", "name_en": "Suspensions"},
        {"name": "قطع ميكانيكية", "name_en": "Mechanical"},
        {"name": "قطع غير مصنفة", "name_en": "Uncategorized"},
    ]

    for item in categories:
        category_object = Category(name=item["name"], name_en=item["name_en"])
        category_object.save()

    return redirect("main:home_view")


@transaction.atomic
def save_parts_to_database(request: HttpRequest):
    # Add parts to the database
    parts_data = [
        {"part_category_id": 1, "image": "engine.jpg", "name": "مكينة", "alternative_name": "مكاين مكينة مكنة مكينه مكنه"},
        {"part_category_id": 1, "image": "transfer_case.jpg", "name": "دبل", "alternative_name": "الدبل دبل"},
        {"part_category_id": 1, "image": "transmission.jpg", "name": "قير", "alternative_name": "قيربوكس جير جيربوكس قربوكس جربوكس القير القيربوكس الجربوكس الجيربوكس"},
        {"part_category_id": 2, "image": "starter.jpg", "name": "سلف", "alternative_name": "سلف مرش السلف المرش"},
        {"part_category_id": 2, "image": "wiper_motor.jpg", "name": "دينمو مساحات", "alternative_name": "دنمو مساحات مكينة مساحات مكينه مساحات دينمو مساحه دينمو مساحة"},
        {"part_category_id": 2, "image": "ignition_switch.jpg", "name": "سويتش", "alternative_name": "سويتش سوتش دقمه دقمة سستم تشغيل سيستم تشغيل مفتاح ايموبلايزر"},
        {"part_category_id": 2, "image": "alternator.jpg", "name": "دينامو", "alternative_name": "دينمو دنمو دينامو شحن دنمو شحن داينمو تعبئة"},
        {"part_category_id": 3, "image": "bumber_front.jpg", "name": "صدام أمامي", "alternative_name": "صدام امامي صدم أمامي"},
        {"part_category_id": 3, "image": "bumber_rear.jpg", "name": "صدام خلفي", "alternative_name": "صدم خلفي صدام"},
        {"part_category_id": 3, "image": "door_back.jpg", "name": "باب خلفي", "alternative_name": "بيبان خلفية أبواب خلفيه ابواب خلفية"},
        {"part_category_id": 3, "image": "door_front.jpg", "name": "باب أمامي", "alternative_name": "بيبان امامي ابواب امامي"},
        {"part_category_id": 4, "image": "headlight.jpg", "name": "شمعة", "alternative_name": "شمعات شمعه"},
        {"part_category_id": 4, "image": "tail_light.jpg", "name": "سطب خلفي", "alternative_name": "اسطب سطبات خلفيه سطبات خلفية"},
        {"part_category_id": 4, "image": "fog_lights.jpg", "name": "كشاف", "alternative_name": "كشافات كشاف ضباب كشاف تحت"},
        {"part_category_id": 5, "image": "compressor.jpg", "name": "كمبروسر", "alternative_name": "كومبرسور كمبروسور كمبرسر"},
        {"part_category_id": 5, "image": "radiator.jpg", "name": "راديتر", "alternative_name": "رديتر رادتر رديترات رديترات"},
        {"part_category_id": 5, "image": "cooling_fan.jpg", "name": "مراوح تبريد", "alternative_name": "مروحة مروحه "},
        {"part_category_id": 6, "image": "seat_rear.jpg", "name": "مرتبة خلفية", "alternative_name": "مرتبه مراتب خلفية مراتب خلفيه مرتبه ثانية مرتبة ثانية"},
        {"part_category_id": 6, "image": "seat_front.jpg", "name": "مرتبة أمامية", "alternative_name": "مرتبه امامية مرتبة اماميه"},
        {"part_category_id": 6, "image": "speedometer.jpg", "name": "عداد طبلون", "alternative_name": ""},
        {"part_category_id": 7, "image": "lower_control.jpg", "name": "مقصات", "alternative_name": "مقص"},
        {"part_category_id": 7, "image": "axle_shaft.jpg", "name": "عكس", "alternative_name": "عكوس"},
        {"part_category_id": 7, "image": "shock_absorber.jpg", "name": "مساعد", "alternative_name": "مساعدات"},
        {"part_category_id": 8, "image": "abs.jpg", "name": "جهاز ABS", "alternative_name": ""},
        {"part_category_id": 8, "image": "frame.jpg", "name": "شاصية المكينة", "alternative_name": "شاصيه مكينه"},
        {"part_category_id": 8, "image": "drive_shaft.jpg", "name": "عمود دبل", "alternative_name": ""},
        {"part_category_id": 9, "image": "default.svg", "name": "كونسول", "alternative_name": ""},
    ]

    parts_to_save = []
    for part_data in parts_data:
        part = Part(
            part_category_id=part_data["part_category_id"],
            name=part_data["name"],
            image=f"parts_images/{part_data['image']}"
        )
        parts_to_save.append(part)

    # Bulk create all parts at once to optimize database operations
    Part.objects.bulk_create(parts_to_save)

    return redirect("main:home_view")



@transaction.atomic
def save_products_to_database(request: HttpRequest):
    # First delete all existing products
    Product.objects.all().delete()
    
    # Reset the SQLite sequence
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='autoparts_product';")

    # Parts that should have direction
    parts_with_direction = [
        "صدام أمامي", "صدام خلفي", "باب خلفي", "باب أمامي", 
        "شمعة", "سطب خلفي", "كشاف",
        "مرتبة خلفية", "مرتبة أمامية",
        "مقصات", "عكس", "مساعد"
    ]

    # Get all parts
    parts = Part.objects.all()
    # Get cars for assignment
    cars = Car.objects.all()
    # Get a seller (you'll need to ensure this exists)
    seller = ProfileSeller.objects.first()

    conditions = ["نظيف", "شبه جديد", "نظيف جداً"]
    made_in = ["الصين", "كوري", "اليابان"]
    
    products_to_create = []
    
    for part in parts:
        # Create 3 products for each part
        for i in range(3):
            # Generate random dates within constraints
            start_year = random.choice([2018, 2019, 2020, 2021])
            end_year = min(start_year + random.randint(1, 3), 2024)
            
            # Generate image name using English characters only
            image_name = f"product_{i + 1}_{random.randint(1000, 9999)}.jpg"
            image_path = "products_images/default.svg" if random.choice([True, False]) else f"products_images/{image_name}"
            
            # Get alternative names if they exist
            alt_names = part.alternative_name.split() if part.alternative_name else []
            description = f"قطع غيار {part.name} " + (f"({random.choice(alt_names)})" if alt_names else "")
            
            # Only assign direction if part is in the direction list
            part_direction = None
            if part.name in parts_with_direction:
                part_direction = random.choice([Product.PartDirection.RIGHT, Product.PartDirection.LEFT])
            
            product = Product(
                part=part,
                seller=seller,
                name=f"{part.name} - {i + 1}",
                part_direction=part_direction,
                made=random.choice([*made_in, None]),
                stock=random.randint(1, 10),
                condition=random.choice(conditions),
                start_date=start_year,
                end_date=end_year,
                price=random.randint(100, 5000),
                delivery_cost=None,
                description=description,
                image=image_path
            )
            products_to_create.append(product)
    
    # Bulk create all products
    products = Product.objects.bulk_create(products_to_create)
    
    # Add cars to products (since we can't do this in bulk_create with M2M)
    for product in products:
        # Randomly assign 1-3 cars to each product
        product_cars = random.sample(list(cars), random.randint(1, min(3, len(cars))))
        product.car.add(*product_cars)

    return redirect("main:home_view")






@transaction.atomic
def save_myproducts_to_database(request):
    # First delete all existing products
    Product.objects.all().delete()
    
    # Reset the SQLite sequence
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='autoparts_product';")

    # Get a seller (you'll need to ensure this exists)
    seller = ProfileSeller.objects.get(id=1)  # Assuming seller id 1 exists

    # Read products data
    products_data = []
    products_car_relations = []

    # Read main products CSV
    with open(os.path.join(settings.BASE_DIR, 'autoparts_product.csv'), 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            products_data.append({
                'id': int(row['id']),
                'part_id': int(row['part_id']),
                'seller_id': int(row['seller_id']),
                'name': row['name'],
                'part_direction': row['part_direction'] if row['part_direction'] else None,
                'made': row['made'] if row['made'] != 'None' else None,
                'stock': int(row['stock']),
                'condition': row['condition'],
                'start_date': int(row['start_date']),
                'end_date': int(row['end_date']),
                'price': int(row['price']),
                'delivery_cost': int(row['delivery_cost']) if row['delivery_cost'] else None,
                'description': row['description'],
                'image': row['image']
            })

    # Read product-car relations CSV
    with open(os.path.join(settings.BASE_DIR, 'autoparts_product_car.csv'), 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            products_car_relations.append({
                'product_id': int(row['product_id']),
                'car_id': int(row['car_id'])
            })

    # Create products
    products_to_create = []
    for data in products_data:
        product = Product(
            id=data['id'],
            part_id=data['part_id'],
            seller=seller,  # Use the seller we got earlier
            name=data['name'],
            part_direction=data['part_direction'],
            made=data['made'],
            stock=data['stock'],
            condition=data['condition'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            price=data['price'],
            delivery_cost=data['delivery_cost'],
            description=data['description'],
            image=data['image']
        )
        products_to_create.append(product)

    # Bulk create all products
    created_products = Product.objects.bulk_create(products_to_create)

    # Add car relations
    for relation in products_car_relations:
        product = Product.objects.get(id=relation['product_id'])
        car = Car.objects.get(id=relation['car_id'])
        product.car.add(car)

    return redirect("main:home_view")
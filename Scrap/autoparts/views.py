from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.db import transaction
from .models import Category, Part, Product

# Create your views here.
def all_parts_view(request: HttpRequest):
    categories = Category.objects.all()
    parts = Part.objects.all()
    context = {"categories": categories}

    return render(request, "autoparts/all_parts.html", context)


def products_view(request: HttpRequest, part_id):
    chosen_part = Part.objects.get(pk=part_id)
    products = Product.objects.all().filter(part=chosen_part)
    context = {"products": products}

    return render(request, "autoparts/products.html", context)


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
        {"name": "المحركات / المكينة والقير", "name_en": "Engine & Transmission"},
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
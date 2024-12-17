import phonenumbers
from phonenumbers import NumberParseException
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.contrib.auth import authenticate, login, logout
from accounts.models import ProfileSeller
from autoparts.models import Category
from Vehicle.models import Brand

from autoparts.models import Category

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

import phonenumbers

def sign_up(request: HttpRequest):
    if request.method == "POST":
        phone_number = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email", "")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        
        phone_regex = RegexValidator(
            regex=r'^05\d{8}$',
            message="رقم الجوال يجب ان يبدأ ب05 وأن يحتوي 10 ارقام"
        )
        
        try:
            phone_regex(phone_number)
            
            parsed_phone = phonenumbers.parse(phone_number, "SA") 
            e164_phone = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
            
            if User.objects.filter(username=e164_phone).exists():
                messages.error(request, "الرقم مسجل مسبقًا!", "alert-danger")
                return render(request, "accounts/signup.html")
            
            with transaction.atomic():
                new_user = User.objects.create_user(username=e164_phone,
                                                    password=password,
                                                    email=email, 
                                                    first_name=first_name, 
                                                    last_name=last_name)

                
                profile_customer = ProfileCustomer(user=new_user, neighborhood=neighborhood, phone_number=e164_number)
                profile_customer.save()
                
                if not new_user.groups.filter(name='customers').exists():
                    group = Group.objects.get(name="customers")
                    new_user.groups.add(group)
                else:
                    print("User already in 'customers' group")
                
                messages.success(request, "تم التسجيل بنجاح!", "alert-success")
                return redirect("accounts:sign_in")
        except ValidationError as e:
            messages.error(request, "رقم الجوال يجب ان يبدأ ب05 وأن يحتوي 10 ارقام", "alert-danger")
            # return render(request, "accounts/signup.html")
        except phonenumbers.NumberParseException:
            messages.error(request, "رقم الجوال يجب ان يبدأ ب05 وأن يحتوي 10 ارقام", "alert-danger")
            # return render(request, "accounts/signup.html")
        except Exception as e:
            messages.error(request, "حصل خطأ، حاول مرة اخرى!", "alert-danger")
            print(e)

    return render(request, "accounts/signup.html")

def sign_in(request: HttpRequest):
    if request.method == "POST":
        phone_number = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        
        phone_regex = RegexValidator(
            regex=r'^05\d{8}$',
            message="رقم الجوال يجب ان يبدأ ب05 وأن يحتوي 10 ارقام"
        )
        
        try:
            phone_regex(phone_number)
            
            parsed_phone = phonenumbers.parse(phone_number, "SA") 
            e164_phone = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
            
            if User.objects.filter(username=e164_phone).exists():
                messages.error(request, "الرقم مسجل مسبقًا!", "alert-danger")
                return render(request, "accounts/seller_signup.html", {
                    'brands': brands, 
                    'specializaties': specializaties
                })
                
            with transaction.atomic():
                new_user = User.objects.create_user(username=e164_phone,
                                                    password=password,
                                                    first_name=first_name)
                
                # Create seller profile form instance
                seller_form = ProfileSellerForm(request.POST)
                if seller_form.is_valid():
                    # Save the seller profile but attach user after saving
                    profile = seller_form.save(commit=False)
                    profile.user = new_user
                    profile.save()
                    
                    if not new_user.groups.filter(name='sellers').exists():
                        group = Group.objects.get(name="sellers")
                        new_user.groups.add(group)
                    else:
                        print("user in sellers group")
                    
                    messages.success(request, "تم التسجيل بنجاح!", "alert-success")
                    return redirect("accounts:sign_in")
                else:
                    messages.error(request, "يرجى تصحيح الأخطاء في النموذج.", "alert-danger")

        except ValidationError as e:
            messages.error(request, "رقم الجوال يجب ان يبدأ ب05 وأن يحتوي 10 ارقام", "alert-danger")
        except phonenumbers.NumberParseException:
            messages.error(request, "رقم الجوال يجب ان يبدأ ب05 وأن يحتوي 10 ارقام", "alert-danger")
        except Exception as e:
            messages.error(request, "حصل خطأ، حاول مرة اخرى!", "alert-danger")
            print(e)

    return render(request, "accounts/seller_signup.html", {
        'brands': brands, 
        'specializaties': specializaties
    })


def sign_in(request: HttpRequest):
    if request.method == "POST":
        phone_number = request.POST.get("username")
        password = request.POST.get("password")
        notify = request.POST.get("notify") == "1" 

        try:
            if notify:
                parsed_phone = phonenumbers.parse(phone_number, "SA")  
                e164_phone = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)

                user = authenticate(request, username=e164_phone, password=password)
            else:
                user = authenticate(request, username=phone_number, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "تم تسجيل الدخول بنجاح", "alert-success")
                return redirect(request.GET.get("next", "/"))
            else:
                messages.error(request, "رقم الجوال أو كلمة المرور غير صحيحة", "alert-danger")
        except phonenumbers.NumberParseException:
            messages.error(request, "رقم الجوال غير صالح. يرجى إدخال رقم يبدأ بـ '05' من 10 أرقام.", "alert-danger")

    return render(request, "accounts/signin.html")


def log_out(request: HttpRequest):

    logout(request)
    messages.success(request, "تم تسجيل الخروج بنجاح!", "alert-warning")

    return redirect(request.GET.get("next", "/"))

# def update_user_profile(request:HttpRequest):

#     if not request.user.is_authenticated:
#         messages.warning(request, "Only registered users can update their profile", "alert-warning")
#         return redirect("accounts:sign_in")
    

#     if request.method == "POST":

#         try:
#             with transaction.atomic():
#                 user:User = request.user
#                 profile_seller = ProfileSeller(user=new_user, specialized=request.POST["specialized"], company_name=request.POST["company_name"], google_map_address=request.POST["google_map_address"], address=request.POST["address"], commercial_register=request.POST["commercial_register"])


#             messages.success(request, "updated profile successfuly", "alert-success")
#         except Exception as e:
#             messages.error(request, "Couldn't update profile", "alert-danger")
#             print(e)

#     return render(request, "accounts/update_profile.html")
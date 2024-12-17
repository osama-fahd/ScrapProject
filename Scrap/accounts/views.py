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

def seller_sign_up(request: HttpRequest):
    brands = Brand.objects.all()
    specializaties = Category.objects.all()
    
    if request.method == "POST":
        username = request.POST.get("username") 
        phone_number = request.POST.get("phone_number")  
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        company_name = request.POST.get("company_name")
        commercial_register = request.POST.get("commercial_register")
        google_map_address = request.POST.get("google_map_address")
        address = request.POST.get("address")
        brands_selected = request.POST.getlist("brands")
        specializaties_selected = request.POST.getlist("specializaties")
        email = request.POST.get("email", "")

        print("DEBUG: username:", username)
        print("DEBUG: phone_number (raw):", phone_number)

        try:
            raw_number = ''.join(filter(str.isdigit, phone_number))
            print("DEBUG: raw_number (digits only):", raw_number)

            if len(raw_number) < 9:
                print("DEBUG: raw_number length:", len(raw_number))
                raise ValueError("الرقم قصير جداً، يرجى إدخال رقم صحيح.")
            
            if raw_number.startswith('0'):
                raw_number = raw_number[1:]  
            
            print("DEBUG: raw_number after removing leading zero:", raw_number)

            sa_number = f"+966{raw_number}"
            print("DEBUG: sa_number:", sa_number)


            parsed_number = phonenumbers.parse(sa_number, "SA")
            print("DEBUG: parsed_number:", parsed_number)

            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("رقم الجوال غير صالح.")

            e164_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            print("DEBUG: e164_number:", e164_number)

        except (ValueError, NumberParseException) as e:
            messages.error(request, f"رقم الجوال غير صالح: {e}", "alert-danger")
            return render(request, "accounts/seller_signup.html", {
                'brands': brands,
                'specializaties': specializaties
            })

        try:
            with transaction.atomic():
                new_user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    email=email
                )

                profile = ProfileSeller.objects.create(
                    user=new_user,
                    company_name=company_name,
                    commercial_register=commercial_register,
                    google_map_address=google_map_address,
                    address=address,
                    phone_number=e164_number
                )

                profile.brands.set(brands_selected)
                profile.specializaties.set(specializaties_selected)
                profile.save()

                group, created = Group.objects.get_or_create(name='sellers')
                new_user.groups.add(group)

            messages.success(request, "تم التسجيل بنجاح!", "alert-success")
            return redirect("accounts:sign_in")

        except IntegrityError as e:
            messages.error(request, "الرقم مسجل مسبقًا!", "alert-danger")
            print("DEBUG (IntegrityError):", e)
        except Exception as e:
            messages.error(request, "حصل خطأ، حاول مرة اخرى!", "alert-danger")
            print("DEBUG (Exception):", e)

    return render(request, "accounts/seller_signup.html", {
        'brands': brands, 
        'specializaties': specializaties
    })

def sign_up(request: HttpRequest):
    if request.method == "POST":

        username = request.POST.get("username")  
        phone_number = request.POST.get("phone_number") 
        password = request.POST.get("password")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        neighborhood = request.POST.get("neighborhood")

        try:
            raw_number = ''.join(filter(str.isdigit, phone_number))
            
            if raw_number.startswith('0'):
                raw_number = raw_number[1:]
            else:
                raise ValueError("يجب أن يبدأ رقم الجوال بالصفر.")
            
            sa_number = f"+966{raw_number}"
            
            parsed_number = phonenumbers.parse(sa_number, "SA")
            
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("رقم الجوال غير صالح.")
            
            e164_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except Exception as e:
            messages.error(request, f"رقم الجوال غير صالح: {e}", "alert-danger")
            return render(request, "accounts/signup.html")

        try:
            with transaction.atomic():
                new_user = User.objects.create_user(
                    username=username,  
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                new_user.save()
                
                profile_customer = ProfileCustomer(user=new_user, neighborhood=neighborhood, phone_number=e164_number)
                profile_customer.save()
                
                if not new_user.groups.filter(name='customers').exists():
                    group = Group.objects.get(name="customers")
                    new_user.groups.add(group)
                else:
                    print("User already in 'customers' group")
                
            messages.success(request, "تم التسجيل بنجاح!", "alert-success")
            return redirect("accounts:sign_in")
        except IntegrityError:
            messages.error(request, "الرقم مسجل مسبقًا!", "alert-danger")
        except Exception as e:
            messages.error(request, "حصل خطأ، حاول مرة اخرى!", "alert-danger")
            print(e)

    return render(request, "accounts/signup.html")

def sign_in(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")  
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "تم تسجيل الدخول بنجاح", "alert-success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "حصل خطأ، حاول مرة اخرى!", "alert-danger")

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
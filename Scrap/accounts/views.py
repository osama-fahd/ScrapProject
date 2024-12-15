from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError, transaction

from .models import ProfileCustomer, ProfileSeller
from .forms import ProfileSellerForm

from Vehicle.models import Brand

def sign_up(request: HttpRequest):
    if request.method == "POST":

        try:
            with transaction.atomic():
                new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
                new_user.save()
                
                #Creating Customer Profile 
                profile_customer = ProfileCustomer(user=new_user, neighborhood=request.POST["neighborhood"])
                profile_customer.save()
                
            messages.success(request, "تم التسجيل بنجاح!", "alert-success")
            return redirect("accounts:sign_in")
        except IntegrityError as e:
            messages.error(request, "الرقم مسجل مسبقًا!", "alert-danger")
        except Exception as e:
            messages.error(request, "حصل خطأ، حاول مرة اخرى!", "alert-danger")
            print(e)

    return render(request, "accounts/signup.html")


def seller_sign_up(request: HttpRequest):
    brands = Brand.objects.all()
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                # Create the user
                new_user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password"],
                    first_name=request.POST["first_name"]
                )
                
                # Create seller profile form instance
                seller_form = ProfileSellerForm(request.POST)
                if seller_form.is_valid():
                    # Save the seller profile but attach user after saving
                    profile = seller_form.save(commit=False)
                    profile.user = new_user
                    profile.save()
                    
                    messages.success(request, "تم التسجيل بنجاح!", "alert-success")
                    return redirect("accounts:sign_in")
                else:
                    messages.error(request, "يرجى تصحيح الأخطاء في النموذج.", "alert-danger")

        except IntegrityError:
            messages.error(request, "الرقم مسجل مسبقًا!", "alert-danger")
        except Exception as e:
            messages.error(request, "حصل خطأ، حاول مرة اخرى!", "alert-danger")
            print(e)

    return render(request, "accounts/seller_signup.html", {
        'brands': brands, 
        'specialized': ProfileSeller.Specialization.choices
    })



def sign_in(request:HttpRequest):
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])

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
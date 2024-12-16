from django.shortcuts import redirect,render
from django.http import HttpRequest  
from django.contrib import messages
from accounts.models import ProfileCustomer  
from .models import Cart, CartItem, Product
from django.db import transaction
from django.contrib.auth.models import User



def profile_customer(request:HttpRequest):
   if not request.user.is_authenticated:
      messages.warning(request, "يمكن فقط للمستخدمين المسجلين رؤية ملف الشخصي", "alert-warning")
      return redirect("accounts:sign_in")
    
   
   profile =  ProfileCustomer.objects.get(user=request.user)

 
   return render(request, 'customer/profile_customer.html',{'profile': profile})

def update_profile(request:HttpRequest):
   if not request.user.is_authenticated:
      messages.warning(request, "Only registered users can update their profile", "alert-warning")
      return redirect("accounts:sign_in")
   
   if request.method == "POST":
      try:
         with transaction.atomic():
               
               user:User = request.user
               user.username = request.POST["username"]
               user.first_name = request.POST["first_name"]
               user.last_name = request.POST["last_name"]
               user.email = request.POST["email"]
               user.save()

               profile:ProfileCustomer = ProfileCustomer.objects.get(user=request.user)
               profile.neighborhood = request.POST["neighborhood"]
               profile.save()

               messages.success(request, "تم تحديث الملف الشخصي بنجاح.", "alert-success")
               return redirect("customer:profile_customer")
      except Exception as e:
         messages.error(request, "تعذر تحديث الملف الشخصي. حاول مرة أخرى.", "alert-danger")
         print(f"Error during profile update: {e}")

   return render(request, "customer/update_profile.html")



def view_cart(request: HttpRequest):

   if not request.user.is_authenticated:
      messages.warning(request, "يمكن فقط للمستخدمين المسجلين رؤية عربة التسوق", "alert-warning")
      return redirect("accounts:sign_in")
   
   profile_customer = ProfileCustomer.objects.get(user=request.user)
   cart, created = Cart.objects.get_or_create(customer=profile_customer)
   cart_items = CartItem.objects.filter(cart=cart)
   total_price = sum(item.product.price * item.quantity for item in cart_items)
   total_items = sum(item.quantity for item in cart_items)

   if created:
      messages.success(request, "لقد تم إنشاء عربة جديدة لك.", "alert-success")

   context = {
      "cart": cart,
      "cart_items": cart_items,
      "total_price": total_price,
      "total_items": total_items,
   }
   return render(request, "customer/view_cart.html", context)


def add_cart(request: HttpRequest, product_id: int):
   try:
      product = Product.objects.get(pk=product_id)

      profile_customer = ProfileCustomer.objects.get(user=request.user)

      cart, created = Cart.objects.get_or_create(customer=profile_customer)

      cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

      if not created:
         cart_item.quantity += 1
         messages.success(request, f"تمت أضافة المنتج الي عربة التسوق الخاصة بك." , "alert-success")
         cart_item.save()

      return redirect('customer:view_cart')
   except Exception as e:
      messages.error(request, f"حدث خطأ: {e}", "alert-danger")
      return redirect("main:home_view")


def remove_from_cart(request: HttpRequest, cart_item_id: int):
   cart_item = CartItem.objects.get(pk=cart_item_id)
   messages.success(request, f"تمت إزالة المنتج من سلة التسوق الخاصة بك." , "alert-success")
   cart_item.delete()
   return redirect('customer:view_cart')



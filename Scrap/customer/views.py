from django.shortcuts import redirect,render
from django.http import HttpRequest  
from django.contrib import messages
from accounts.models import ProfileCustomer  
from .models import Cart, CartItem, Product
from django.db import transaction
from django.contrib.auth.models import User
from sellers.models import OrderItem



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
   if not request.user.is_authenticated:
      messages.warning(request, "يمكن فقط للمستخدمين المسجلين رؤية عربة التسوق", "alert-warning")
      return redirect("accounts:sign_in")
   
   try:
      product = Product.objects.get(pk=product_id)

      profile_customer = ProfileCustomer.objects.get(user=request.user)

      cart, created = Cart.objects.get_or_create(customer=profile_customer)

      cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

      if not created:
         if cart_item.quantity + 1 > product.stock:
               messages.error(request, f"عذرًا، الكمية المطلوبة تتجاوز المخزون المتوفر ({product.stock}).", "alert-danger")
               return redirect('customer:view_cart')
         cart_item.quantity += 1
      else:
         if 1 > product.stock:
            messages.error(request, f"عذرًا، المنتج غير متوفر بالمخزون.", "alert-danger")
            return redirect('main:home_view')
        
      cart_item.save()
      
      messages.success(request, "تمت إضافة المنتج إلى عربة التسوق الخاصة بك.", "alert-success")
      # Check if there's a next parameter
      next_url = request.GET.get('next')
      if next_url:
         return redirect(next_url)
      return redirect('customer:view_cart')
   except Exception as e:
      messages.error(request, f" حدث خطأ: {e}", "alert-danger")
      return redirect("main:home_view")


def remove_from_cart(request: HttpRequest, cart_item_id: int):
   cart_item = CartItem.objects.get(pk=cart_item_id)
   messages.success(request, f"تمت إزالة المنتج من سلة التسوق الخاصة بك." , "alert-success")
   cart_item.delete()
   return redirect('customer:view_cart')


def increase_quantity(request: HttpRequest, cart_item_id: int):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        product = cart_item.product

        if cart_item.quantity + 1 > product.stock:
            messages.error(request, f"عذرًا، الكمية المطلوبة تتجاوز المخزون المتوفر ({product.stock}).", "alert-danger")
        else:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "تمت زيادة الكمية بنجاح.", "alert-success")

        return redirect('customer:view_cart')
    except CartItem.DoesNotExist:
        messages.error(request, "عنصر السلة غير موجود.", "alert-danger")
        return redirect('main:home_view')
    except Exception as e:
        messages.error(request, f"حدث خطأ: {e}", "alert-danger")
        return redirect('main:home_view')


def decrease_quantity(request: HttpRequest, cart_item_id: int):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)

        if cart_item.quantity - 1 < 1:
            messages.error(request, "لا يمكن أن تكون الكمية أقل من 1.", "alert-danger")
        else:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, "تمت إنقاص الكمية بنجاح.", "alert-success")

        return redirect('customer:view_cart')
    except CartItem.DoesNotExist:
        messages.error(request, "عنصر السلة غير موجود.", "alert-danger")
        return redirect('main:home_view')
    except Exception as e:
        messages.error(request, f"حدث خطأ: {e}", "alert-danger")
        return redirect('main:home_view')




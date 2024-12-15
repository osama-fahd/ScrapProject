from django.urls import path
from . import views

app_name = "customer"

urlpatterns = [
    path("profile_customer/", views.profile_customer, name="profile_customer"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("cart/", views.view_cart, name="view_cart"),
    path("add_cart/<product_id>/", views.add_cart, name="add_cart"),
    path("remove_from_cart/<cart_item_id>/", views.remove_from_cart, name="remove_from_cart"),

]
from django.urls import path
from . import views
app_name = "Vehicle"
urlpatterns = [
    path("brand/", views.new_brand, name="new_brand"),
    path("car/", views.new_car, name="new_car"),
    path("save_brands_to_database/", views.save_brands_to_database, name="save_brands_to_database"),
    path("save_cars_to_database/", views.save_cars_to_database, name="save_cars_to_database"),


]
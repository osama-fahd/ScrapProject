from django.urls import path
from . import views
app_name = "Vehicle"
urlpatterns = [
    path("brand/", views.new_brand, name="new_brand"),
    path("car/", views.new_car, name="new_car"),

]
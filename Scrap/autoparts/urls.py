from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("all_parts/", views.all_parts_view, name="all_parts_view"),
    path("products/", views.products_view, name="products_view"),
    path("save_categories_to_database/", views.save_categories_to_database, name="save_categories_to_database"),
    path("save_parts_to_database/", views.save_parts_to_database, name="save_parts_to_database"),
]
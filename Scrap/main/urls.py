from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('form_example/', views.form_example, name="form_example"),
    path('content_example/', views.content_example, name="content_example"),
    path('contact/', views.contact_view, name="contact_view"),
]
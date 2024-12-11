from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.sign_up, name="sign_up"),
    path('seller_signup/', views.seller_sign_up, name="seller_sign_up"),
    path('signin/', views.sign_in, name="sign_in"),
    path('logout/', views.log_out, name="log_out"),
]
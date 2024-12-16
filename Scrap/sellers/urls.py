from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    # path('profile/<int:user_id>/', views.seller_profile_products, name='seller_profile_products'),
    path('add-product/', views.seller_add_product, name='seller_add_product'),
    path('update/<int:product_id>/', views.update_product, name='update_product'),
    # path('inventory/', views.seller_stock, name='seller_stock'),
    path('delete/<int:product_id>/', views.seller_add_product, name='delete_product'),
    path('profile/<int:seller_id>/', views.seller_profile_view, name='seller_profile'),


]

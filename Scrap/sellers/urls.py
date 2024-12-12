from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    # path('products/', views.seller_products, name='seller_products'),
    path('add-product/', views.seller_add_product, name='seller_add_product'),
    path('inventory/', views.seller_stock, name='seller_stock'),

]

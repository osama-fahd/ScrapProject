from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    # path('profile/<int:user_id>/', views.seller_profile_products, name='seller_profile_products'),
    path('add-product/', views.seller_add_product, name='seller_add_product'),
    path('update/<int:product_id>/', views.update_product, name='update_product'),
    # path('inventory/', views.seller_stock, name='seller_stock'),
    # path('delete/<int:product_id>/', views.seller_delete_product, name='seller_delete_product'),
    path('profile/<int:seller_id>/', views.seller_profile_view, name='seller_profile_view'),
    path('orders/', views.seller_order_list_view, name='seller_order_list_view'),
    path('orders/accept/<int:order_item_id>/', views.accept_order_item, name='accept_order_item'),
    path('orders/deny/<int:order_item_id>/', views.deny_order_item, name='deny_order_item'),
    path('accepted_orders/', views.accepted_order_list_view, name='accepted_order_list_view'),
    path('order_detail/<int:order_item_id>/', views.order_detail_view, name='order_detail_view'),
    path('order_detail/<int:order_item_id>/mark_delivered/', views.mark_as_delivered_view, name='mark_as_delivered_view'),
    path('delivered_history/', views.delivered_orders_history_view, name='delivered_orders_history_view'),
    path('checkout/', views.checkout, name='checkout'),




]

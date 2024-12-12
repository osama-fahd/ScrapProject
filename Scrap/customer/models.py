from django.db import models
from autoparts.models import Product  
from django.contrib.auth.models import User
from accounts.models import ProfileCustomer, ProfileSeller
# Create your models here.


class Cart(models.Model):
    customer = models.ForeignKey(ProfileCustomer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class OrderHistorty(models.Model):
    sellers = models.ForeignKey(ProfileSeller, on_delete=models.CASCADE)
    customer = models.ForeignKey(ProfileCustomer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)


class CustomerSellersHistorty(models.Model):
    sellers = models.ForeignKey(ProfileSeller, on_delete=models.CASCADE,  unique=True)
    customer = models.OneToOneField(ProfileCustomer, on_delete=models.CASCADE)
from django.db import models
from django.contrib.auth.models import User
from Vehicle.models import Car,Brand
from autoparts.models import Product
from accounts.models import ProfileCustomer , ProfileSeller
from customer.models import Cart


# Create your models here.


class OrderItem(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'انتظار مراجعة البائع'
        ACCEPTED = 'ACCEPTED', 'قيد التوصيل'
        # IN_PROGRESS = 'IN_PROGRESS', 'قيد العمل'
        DELIVERED = 'DELIVERED', 'تم التوصيل'
        DENIED = 'DENIED', 'رفض'
    
    status = models.CharField(
        max_length=20,choices=Status.choices,default=Status.PENDING)
    # product = models.ForeignKey(
        # Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        ProfileCustomer, null=True, on_delete=models.PROTECT)
    seller = models.ForeignKey(
        ProfileSeller, null=True, on_delete=models.PROTECT)
    date_created = models.DateTimeField(
        auto_now_add=True, null=True)



    
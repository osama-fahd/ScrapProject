from django.db import models
from django.contrib.auth.models import User
from Vehicle.models import Car,Brand
from autoparts.models import Product
from accounts.models import ProfileCustomer , ProfileSeller
# from customer.models import Cart


# Create your models here.


class OrderItem(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        OUT_FOR_DELIVERY = 'Out for Delivery', 'Out for Delivery'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        DENIED = 'DENIED', 'Denied'

    status = models.CharField(
        max_length=20,choices=Status.choices,default=Status.PENDING)

    customer = models.ForeignKey(
        ProfileCustomer, null=True, on_delete=models.PROTECT)

    # cart = models.ForeignKey(
    #     Cart, null=True, on_delete=models.PROTECT)

    date_created = models.DateTimeField(
        auto_now_add=True, null=True)

class Order(models.Model):
    pass        



    
from django.db import models
from django.contrib.auth.models import User
from Vehicle.models import Car,Brand

# Create your models here.
class ProfileSeller(models.Model):
    # CATEGORY_CHOICES = [
    #     ('bd', 'قطع البودي'),
    #     ('el', 'قطع كهربائية'),
    #     ('mc', 'مكيانيكا'),
    #     ('OT', 'اخرى'),
    # ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    registration_date = models.DateTimeField(auto_now_add=True)

    commercial_register =models.IntegerField()
    

    # national_id=models.IntegerField()

    Company_name= models.CharField(max_length=255)

    address=models.TextField()
    # specialized = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='اختار') 


class Seller(models.Model):
    profile_seller = models.OneToOneField(ProfileSeller, on_delete=models.CASCADE)
    phone = models.CharField(max_length=9, blank=True, null=True)

    def __str__(self):
        return self.profile_seller.company_name

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        OUT_FOR_DELIVERY = 'Out for Delivery', 'Out for Delivery'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        DENIED = 'DENIED', 'Denied'

    status = models.CharField(
        max_length=20,choices=Status.choices,default=Status.PENDING)

    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.PROTECT)

    product = models.ForeignKey(
        Product, null=True, on_delete=models.PROTECT)

    date_created = models.DateTimeField(
        auto_now_add=True, null=True)

    




# class Product(models.Model):
#     # part = models.ForeignKey(Part, on_delete=models.CASCADE)
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     # seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
#     # partDirection = models.CharField(max_length=64,choices=PartDirection.choices,blank=True, null=True)
#     made = models.CharField(max_length=64,blank=True, null=True)
#     stock = models.IntegerField()
#     condition = models.IntegerField()
#     start_date = models.IntegerField()
#     end_date = models.IntegerField()
#     price = models.IntegerField()
#     description = models.CharField(max_length=2000)
#     image = models.ImageField(upload_to="images/")

    
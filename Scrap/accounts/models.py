from django.db import models
from django.contrib.auth.models import User
from Vehicle.models import Brand
from datetime import datetime
# from autoparts.models import Category

from django.apps import apps



# class Specializaty(models.Model):
#     class Specialization(models.TextChoices):
#         ENGINES = "Engine & Transmission", "المكينة والقير"
#         ELECTRICALS = "Electircal",  "قطع كهربائية"
#         EXTERIORS = "Exterior & Body", "البودي"
#         LIGHTS = "lights", "الأنوار"
#         COOLIINGS = "Cooling & Heating", "التبريد والتكييف"
#         INTERIOIR = "Interior & Accessories", "الداخلية والاكسسوارت"
#         SUSPENSIONS = "Suspensions", "الميزانية / نظام التعليق"
#         MECHANICALS = "Mechanical", "قطع ميكانيكية"
#         UNCATEGORIZED = "Uncategorized", "قطع غير مصنفة"
#         ALL = "All", "الكل"
        
#     specialized = models.CharField(max_length=64, choices= Specialization.choices,blank=True, null=True)
    

class ProfileSeller(models.Model):
    def get_categories(self):
        return self.specializaties.all()
    
    specializaties = models.ManyToManyField('autoparts.Category')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
    company_name = models.CharField(max_length=255)
    google_map_address = models.URLField(blank=True)
    address = models.CharField(max_length=300)
    commercial_register = models.IntegerField(max_length=10)
    brands = models.ManyToManyField(Brand)
    
    
    def __str__(self) -> str:
        return f'{self.company_name} - {self.user.username}'
    
    
    
class ProfileCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
    neighborhood = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f'{self.user.first_name} - {self.user.username}'
        
        
        
class Review(models.Model):
    class RatingChoices(models.IntegerChoices):
        star1 = 1, "1"
        star2 = 2, "2"
        star3 = 3, "3"
        star4 = 4, "4"
        star5 = 5, "5"
    
    seller = models.ForeignKey(ProfileSeller, on_delete=models.CASCADE)
    customer = models.ForeignKey(ProfileCustomer, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.SmallIntegerField(choices=RatingChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.customer.first_name} - {self.seller.company_name}'
    

# class Product(models.Model):
#     # part = models.ForeignKey(Part, on_delete=models.CASCADE)
#     car = models.ForeignKey(Car, on_delete=models.CASCADE)
#     seller = models.ForeignKey(ProfileSeller, on_delete=models.CASCADE)
#     # partDirection = models.CharField(max_length=64,choices=PartDirection.choices,blank=True, null=True)
#     made = models.CharField(max_length=64,blank=True, null=True)
    
#     stock = models.IntegerField()
    
#     condition = models.IntegerField()
#     start_date = models.IntegerField()
#     end_date = models.IntegerField()
#     price = models.IntegerField()
#     description = models.CharField(max_length=2000)
#     image = models.ImageField(upload_to="images/")

    
# class Cart(models.Model):
#     customer = models.ForeignKey(ProfileCustomer, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
    
    
# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    
    
# class OrderHistorty(models.Model):
    
    # sellers = models.ForeignKey(ProfileSeller, on_delete=models.CASCADE)
    # customer = models.ForeignKey(ProfileCustomer, on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    

# class CustomerSellersHistorty(models.Model):
#     sellers = models.ForeignKey(ProfileSeller, on_delete=models.CASCADE,  unique=True)
#     customer = models.OneToOneField(ProfileCustomer, on_delete=models.CASCADE)
    
    
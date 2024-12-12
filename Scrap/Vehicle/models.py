from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=250, unique=True)  
    name_en = models.CharField(max_length=250, blank=True, null=True)  
    logo = models.ImageField(upload_to='brand_logos/')

    def __str__(self):
        return self.name
    
class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=250, unique=True) 

    def __str__(self):
        return f"{self.name}"
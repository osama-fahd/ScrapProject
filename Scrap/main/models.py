from django.db import models

class Contact(models.Model):
   
    first_name = models.CharField(max_length=1024)
    username = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.first_name
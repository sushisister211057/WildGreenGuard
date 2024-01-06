from django.db import models

# Create your models here.

class Plant(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to="image/", blank=False)
    species = models.CharField(max_length=50, null=True, blank=True)
    invasion = models.BooleanField(blank=False)
    upload_time = models.DateTimeField(auto_now_add=True)

class Kind(models.Model):
    species = models.CharField(primary_key=True, max_length=50)
    description = models.TextField(max_length=100, blank= False)

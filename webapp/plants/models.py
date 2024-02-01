from django.db import models
from django.utils import timezone

# Create your models here.


class Plant(models.Model):

    imgurl = models.ImageField(upload_to="imgs/")
    scientific_name  = models.CharField(max_length=60) 
    isinvasive = models.BooleanField(null=False)
    description = models.TextField(max_length=200)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.species_chi}, {self.isinvasive}"


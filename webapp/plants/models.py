from django.db import models
from django.utils import timezone

# Create your models here.


class Plant(models.Model):

    species_img = models.ImageField(upload_to="imgs/")
    species_en = models.CharField(max_length=60)
    isinvasive = models.BooleanField()
    description = models.TextField(max_length=200)

    def __str__(self) -> str:
        return f"{self.species_chi}, {self.isinvasive}"


class Record(models.Model):

    uploading = models.FileField(upload_to='uploads/')
    datetime = models.DateTimeField(auto_now_add=True)
    species = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.species.species_chi},{self.datetime.strftime('%Y-%m-%d %H:%M')}"


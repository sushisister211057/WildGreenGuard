from django.db import models
# Create your models here.


class Plant(models.Model):

    species = models.CharField(max_length=100, primary_key=True)
    name_chinese = models.CharField(max_length=30)
    name_english = models.CharField(max_length=60)
    isinvasive = models.BooleanField()
    description = models.TextField(max_length=200)

    def __str__(self) -> str:
        return f"{self.species}, {self.isinvasive}"


class Record(models.Model):

    uploading = models.FileField(upload_to='uploads/')
    datetime = models.DateTimeField(auto_now_add=True)
    species = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.species.name_chinese},{self.datetime.strftime('%Y-%m-%d %H:%M')}"


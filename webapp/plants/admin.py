from django.contrib import admin

from plants.models import Plant, Kind

# Register your models here.

admin.site.register(Plant)
admin.site.register(Kind)

from django.urls import path
from . import views

app_name= "plants"

urlpatterns = [
    path("", views.index, name="index"),
    path("identifier", views.identifier, name="identifier"),
    path("developers", views.developer, name="developers"),
    path("FAQ", views.freq_question, name="questions"),
    path("records", views.records, name="records"),
    path("diagram", views.diagram, name="diagram"),
    path("lan_mode", views.lan_mode, name="lan_mode"),
]
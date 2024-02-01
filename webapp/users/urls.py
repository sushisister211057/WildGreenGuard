from django.urls import path
from . import views

app_name= "users"

urlpatterns = [
    path("line_login", views.line_login, name="line_login"),
]
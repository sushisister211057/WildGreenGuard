from django.urls import path
from . import views

app_name= "users"

urlpatterns = [
    path("line_login", views.line_login, name="line_login"),
    path("logout", views.line_logout, name="line_logout"),
    path("get_access_token", views.get_access_token, name="get_access_token"),
    path("csrf_token", views.csrf_token, name="csrf_token"),
]
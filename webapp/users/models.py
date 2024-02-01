from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractUser, AbstractBaseUser

# Create your models here.

# set up user manager
class CustomUserManager(BaseUserManager):

    def create_user(self, userid, display_name, **extra_fields):
        if not userid or not display_name:
            raise ValueError("userid or name should not be none.")
        user = self.model(userid=userid, display_name=display_name, **extra_fields)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, userid, display_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(userid, display_name, **extra_fields)

# build up custom user model
class CustomUserModel(AbstractBaseUser):
    userid = models.CharField(max_length=33, unique=True)
    display_name = models.CharField(max_length=20, null=False)

    objects= CustomUserManager()

    USERNAME_FIELD = 'userid'
    # for creating superuser
    REQUIRED_FIELDS = ["display_name"]

    def __str__(self):
        return self.display_name
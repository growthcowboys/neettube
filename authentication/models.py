from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone


# Create your models here.

class UserManager(BaseUserManager):


    def create_user(self, email, username, password = None, **kwargs):

        email = self.normalize_email(email)

        user = self.model(email = email, username = username, **kwargs)

        user.set_password(password)

        user.save()

        return user
    
    def create_superuser(self, email, username, password = None, **kwargs):

        email = self.normalize_email(email)

        user = self.model(email = email, username = username, **kwargs)

        user.set_password(password)

        user.is_staff = True
        user.is_superuser = True
        user.date_joined = timezone.now()

        user.save()

        return user



class User(AbstractBaseUser):

    username = models.CharField(
        max_length = 150, 
        unique = True,
        help_text = ("Required. 150 characters or fewer. Letters, and digits only."),
        validators = [UnicodeUsernameValidator(), ],
        error_messages = {
            'unique': ("A user with that username already exists.")
        }
    )
    email = models.EmailField(
        max_length = 225,
        unique = True,
        blank = False,
        null = False,
        error_messages = {
            'unique': ("A user with that email already exists.")
        }
    )

    objects = UserManager()


    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username", ]


    def __str__(self):

        return self.email

    
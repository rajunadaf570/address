#django imports
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _

# app level imports
from libs.models import TimeStampedModel
# from .managers import UserManager


class User(AbstractUser):
    """
    """
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    email = models.EmailField(max_length=128, unique=True, db_index=True, blank=False)
    is_staff = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    def __str__(self):
        return self.username

    @property
    def access_token(self):
        token, is_created = Token.objects.get_or_create(user=self)
        return token.key

    @property
    def full_name(self):
        return "{fn} {ln}".format(fn=self.first_name, ln=self.last_name)

class Address(TimeStampedModel):
    """
    """
    name = models.CharField(max_length=65, blank=True)
    address1 = models.TextField()
    address2 = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user'
    )

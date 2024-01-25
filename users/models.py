from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.db import models
from django.utils import timezone

from .base_user_manager import UtilitiesUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=300)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UtilitiesUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        managed = True
        db_table = "user"

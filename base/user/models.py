from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class Farm(models.Model):
    id = models.CharField(max_length=32, default= uuid.uuid4, primary_key=True,
                          editable=False)
    name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return str(self.name)


class CustomUser(AbstractUser):
    id = models.CharField(max_length=32, default= uuid.uuid4, primary_key=True,
                          editable=False)
    name = models.CharField(max_length=20, null=False)
    farm = models.OneToOneField(Farm, on_delete=models.CASCADE,
                                related_name="owner", null=True, blank=True)
    email = models.EmailField(max_length=50, null=False, unique=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    pix = models.ImageField(null=True, default='default.jpg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self) -> str:
        return str(self.name)

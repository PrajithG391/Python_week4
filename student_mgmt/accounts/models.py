from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    ROLES = (
        ('Admin', 'Admin'),
        ('Student','Student'),
    )

    def __str__(self):
        return self.user.username
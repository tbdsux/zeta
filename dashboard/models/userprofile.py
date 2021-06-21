from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acc_img = models.ImageField(default="profile.png")
    date_joined = models.DateField(auto_now=True)

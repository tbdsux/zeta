from django.db import models
from django.contrib.auth.models import User
import os



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acc_img = models.ImageField(default="profile.png")
    date_joined = models.DateField(auto_now=True)


# Stuffs model
class Stuff(models.Model):
    ITEM_CLASS = (
        ("movie", "Any movie around the world."),
        ("series", "Any series except Asian ones."),
        ("anime", "Anime not cartoons."),
        ("book", "Book"),
        ("manga", "Comics, graphics novels."),
        ("asian drama", "Series from Asia."),
    )

    title = models.CharField(max_length=50)
    classification = models.CharField(max_length=12, choices=ITEM_CLASS)
    web_id = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.title


# Collections
class Collections(models.Model):
    name = models.CharField(max_length=15)
    stuffs = models.ManyToManyField(Stuff, through="Inclution")

    def __str__(self) -> str:
        return self.name


# Inclutions to collections
class Inclution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collections, on_delete=models.CASCADE)
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE)
    date_added = models.DateField()
    added_to = models.CharField(max_length=5)
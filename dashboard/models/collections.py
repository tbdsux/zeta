from django.db import models
from django.contrib.auth.models import User
from nanoid import generate

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
    synopsis = models.TextField()
    img_src = models.CharField(max_length=100)
    classification = models.CharField(max_length=12, choices=ITEM_CLASS)
    web_id = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.title


# Collections
class Collections(models.Model):
    TYPE_CLASS = (
        ("movie", "Any movie around the world."),
        ("series", "Any series except Asian ones."),
        ("anime", "Anime not cartoons."),
        ("book", "Book"),
        ("manga", "Comics, graphics novels."),
        ("asian drama", "Series from Asia."),
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False, default="0"
    )
    collection_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=30, blank=True)
    type = models.CharField(max_length=12, choices=TYPE_CLASS)
    slug = models.SlugField(max_length=7, editable=False)
    stuffs = models.ManyToManyField(Stuff, through="Inclution")
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


# Inclutions to collections
class Inclution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collections, on_delete=models.CASCADE)
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now=True)
    added_to = models.CharField(max_length=7)
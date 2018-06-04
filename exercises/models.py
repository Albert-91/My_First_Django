from django.db import models


# Create your models here.
class Band(models.Model):
    genres = (
        (-1, 'not defined'),
        (0, 'rock'),
        (1, 'metal'),
        (2, 'pop'),
        (3, 'hip - hop'),
        (4, 'electronic'),
        (5, 'reggae'),
        (6, 'other')
    )
    name = models.CharField(max_length=64)
    year = models.IntegerField(null=True)
    still_active = models.BooleanField(default=True)
    genre = models.IntegerField(choices=genres, default=-1)

    def __str__(self):
        return "{}, {}, active: {}, genre: {}".format(self.name, self.year, self.still_active, self.genre)


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)

    def __str__(self):
        return "name: {}, category: {}".format(self.name, self.description)


class Article(models.Model):
    statuses = (
        (1, "In progress"),
        (2, "Awaiting approval"),
        (3, "Published")
    )
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=64, null=True)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=statuses, default=0)
    release_start = models.DateField(null=True)
    release_stop = models.DateField(null=True)
    category = models.ManyToManyField(Category)


class Album(models.Model):
    ratings = zip(range(0, 6), range(0, 6))
    tuple(ratings)
    title = models.CharField(max_length=128)
    year = models.IntegerField()
    rating = models.IntegerField(choices=ratings)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)

    def __str__(self):
        return "title: {}, year: {}, rating: {}".format(self.title, self.year, self.rating)


class Song(models.Model):
    title = models.CharField(max_length=128)
    duration = models.TimeField(null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)


class Genre(models.Model):
    name = models.CharField(max_length=32)


class Movie(models.Model):
    title = models.CharField(max_length=128)
    director = models.ForeignKey(Person, on_delete=models.CASCADE)
    screenplay = models.ForeignKey(Person, on_delete=models.CASCADE)
    starring = models.ManyToManyField(Person)

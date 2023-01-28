from django.db import models


class Ads(models.Model):

    name = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=100)
    is_published = models.BooleanField()


class Categories(models.Model):

    name = models.CharField(max_length=100)
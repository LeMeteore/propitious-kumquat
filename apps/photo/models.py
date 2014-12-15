from django.db import models
from datetime import datetime

class Country(models.Model):
    label = models.CharField(max_length=200)
    def __str__(self):
        return "%s" % self.label


class Pack(models.Model):
    label = models.CharField(max_length=200)
    country = models.ManyToManyField(Country)
    description = models.TextField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return "%s" % self.label

class Photo(models.Model):
    label = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(max_length=200, upload_to='wappa')
    pub_date = models.DateTimeField('date published')
    pack = models.ForeignKey(Pack)

    def __str__(self):
        return "%s" % self.label

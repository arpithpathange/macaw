from django.db import models
import datetime


class savemxevents(models.Model):
    campaign = models.CharField(max_length=200)
    adset = models.CharField(max_length=200)
    ad = models.CharField(max_length=200)
    adv = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    m2 = models.IntegerField(default=0)
    m3 = models.IntegerField(default=0)

class registration(models.Model):
    login = models.CharField(max_length=200)
    passwd = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    adv = models.CharField(max_length=200)
    phone = models.IntegerField(default=0)

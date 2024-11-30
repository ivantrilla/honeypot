from django.db import models
from datetime import date, timedelta, datetime

class UrlPath(models.Model):
    name = models.CharField(max_length=200)
    times_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f'Path with the name : {self.name} and have been used : {self.times_used} times'

class CountryName(models.Model):
    name = models.CharField(max_length=200)
    times_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f'Country with the name : {self.name} and total of {self.times_used} attacks'

class Credential(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    times_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f'Credential with the username: {self.username} and the password: {self.password} have been used {self.times_used} times'

class BadActor(models.Model):
    credenial = models.ManyToManyField(Credential)
    ip_address = models.CharField(max_length=100)
    url_path = models.ManyToManyField(UrlPath)
    country = models.ForeignKey(CountryName,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return f'BadActor with the ip: {self.ip_address} and is from : {self.country}'

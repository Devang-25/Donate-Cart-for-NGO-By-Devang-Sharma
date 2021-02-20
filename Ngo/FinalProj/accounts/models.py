from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Ngo(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    founder = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class NgoRequirementDetail(models.Model):
    ngo = models.ForeignKey(Ngo, on_delete=models.CASCADE)
    req = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.req


class Donator(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.phone


class DonationDetail(models.Model):
    donator = models.ForeignKey(Donator, on_delete=models.CASCADE)
    ngo = models.ForeignKey(Ngo, on_delete=models.CASCADE)
    req = models.CharField(max_length=100, default='')
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.donator)

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class attendance(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class leave(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('denied', 'Denied'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


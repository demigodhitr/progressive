from django.db import models


class  Messages(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    
class Attempts(models.Model):
    failed_attempts = models.IntegerField(default=0)
# Create your models here.

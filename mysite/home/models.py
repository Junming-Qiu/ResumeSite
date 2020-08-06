from django.db import models
from django.utils import timezone
# Create your models here.

class messageModel(models.Model):
    name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=50, default="")
    subject = models.CharField(max_length=100, default="")
    description = models.TextField(default="")
    date_created = models.DateTimeField(auto_now_add=False, default=timezone.now)

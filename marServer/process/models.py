from django.db import models

# Create your models here.
class Operations(models.Model):
    endDate = models.DateField(auto_now_add=True)
    logPath = models.CharField(max_length=250)
    operation = models.CharField(max_length=250, null=True)
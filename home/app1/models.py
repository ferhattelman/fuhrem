from django.db import models

# Create your models here.
class Search_data(models.Model):
    title = models.TextField(null=True)
    tag = models.CharField(max_length=15)
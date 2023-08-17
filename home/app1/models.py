from django.db import models

# Create your models here.
class Search_data(models.Model):
    title = models.TextField(null=True)
    tag = models.CharField(max_length=15)

class Search_history(models.Model):
    value = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    tags = models.TextField()
    datetime = models.DateTimeField()
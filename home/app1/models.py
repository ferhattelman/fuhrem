from django.db import models

# Create your models here.
class Search_data(models.Model):
    title = models.TextField(null=True)
    tag = models.CharField(max_length=15)

class Search_history(models.Model):
    image_type = models.CharField(max_length=15,default='photo')
    value = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    tags = models.TextField()
    search_amount = models.IntegerField(default=12)
    datetime = models.DateTimeField()

    def __str__ (self):
         return f"""
            Sorgu Zamanı = {self.datetime} || 
            Görsel Türü = {self.image_type} || 
            Aranan Kelime = {self.value} || 
            Başlık = {self.title} || 
            Arama Sayısı = {self.search_amount} || 
            Etiketler = {self.tags} || 
           """
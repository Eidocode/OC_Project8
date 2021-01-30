from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    json_id = models.CharField(max_length=200, unique=True)
    url = models.URLField()


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200, default="NC")
    description = models.TextField(default="Aucune description disponible...")
    score = models.CharField(max_length=1)
    barcode = models.CharField(max_length=50, unique=True)
    url_img_small = models.URLField()
    url_img = models.URLField()
    url_off = models.URLField()
    url_img_nutrition = models.URLField()
    categories = models.ManyToManyField(Category, related_name='products')


class Favorite(models.Model):
    added_date = models.DateTimeField(auto_now_add=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('products', 'users',)

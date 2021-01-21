from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    description = models.TextField()
    score = models.CharField(max_length=1)
    barcode = models.CharField(max_length=50)
    url_img= models.URLField()
    categories = models.ManyToManyField(Category, related_name='products')


class Favorite(models.Model):
    added_date = models.DateTimeField(auto_now_add=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)

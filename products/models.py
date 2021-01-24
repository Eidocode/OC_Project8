from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    json_id = models.CharField(max_length=200, default='0000000')
    url = models.CharField(max_length=200, default='https://faekurl.com')


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    score = models.CharField(max_length=1)
    barcode = models.CharField(max_length=50, unique=True)
    url_img = models.URLField()
    categories = models.ManyToManyField(Category, related_name='products')


class Favorite(models.Model):
    added_date = models.DateTimeField(auto_now_add=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)

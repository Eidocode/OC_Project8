# Generated by Django 3.1.5 on 2021-01-30 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('json_id', models.CharField(max_length=200, unique=True)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('brand', models.CharField(default='NC', max_length=200)),
                ('description', models.TextField(default='Aucune description disponible...')),
                ('score', models.CharField(max_length=1)),
                ('barcode', models.CharField(max_length=50, unique=True)),
                ('url_img_small', models.URLField()),
                ('url_img', models.URLField()),
                ('url_off', models.URLField()),
                ('url_img_nutrition', models.URLField()),
                ('categories', models.ManyToManyField(related_name='products', to='products.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('products', 'users')},
            },
        ),
    ]

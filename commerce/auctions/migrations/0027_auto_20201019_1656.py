# Generated by Django 3.1.1 on 2020-10-19 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0026_auto_20201019_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='items',
            field=models.ManyToManyField(to='auctions.Listing', verbose_name='list_item'),
        ),
    ]

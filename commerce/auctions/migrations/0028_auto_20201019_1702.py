# Generated by Django 3.1.1 on 2020-10-19 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_auto_20201019_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='items',
            field=models.ManyToManyField(related_name='list_item', to='auctions.Listing'),
        ),
    ]

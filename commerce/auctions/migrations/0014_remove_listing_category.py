# Generated by Django 3.1.1 on 2020-10-15 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20201015_1845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='category',
        ),
    ]

# Generated by Django 3.1.1 on 2020-10-19 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_auto_20201019_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='item',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bider', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='wishlist_item',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='wishlist_item',
            field=models.ManyToManyField(related_name='list_item', to='auctions.Listing'),
        ),
    ]

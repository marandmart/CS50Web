# Generated by Django 3.1.1 on 2020-10-31 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0036_auto_20201028_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winner',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
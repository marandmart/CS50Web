# Generated by Django 3.1.1 on 2020-10-24 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0029_auto_20201022_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='listing',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='productBids', to='auctions.listing'),
        ),
    ]

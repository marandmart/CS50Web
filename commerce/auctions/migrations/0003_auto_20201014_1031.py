# Generated by Django 3.1.1 on 2020-10-14 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_category_comments_item_category_listing'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]

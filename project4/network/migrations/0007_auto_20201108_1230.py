# Generated by Django 3.1.3 on 2020-11-08 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20201108_1228'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Followers',
            new_name='Follower',
        ),
    ]

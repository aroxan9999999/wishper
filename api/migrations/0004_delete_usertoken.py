# Generated by Django 4.2.6 on 2023-10-08 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_customtoken'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserToken',
        ),
    ]

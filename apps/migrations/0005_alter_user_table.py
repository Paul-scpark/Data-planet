# Generated by Django 4.1.3 on 2022-11-24 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_user_is_authenticated'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='User',
        ),
    ]
# Generated by Django 3.2.7 on 2023-10-12 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resident', '0002_resident_locker'),
    ]

    operations = [
        migrations.AddField(
            model_name='resident',
            name='visited_times',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
# Generated by Django 3.2.7 on 2023-10-13 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resident', '0004_alter_resident_visited_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='resident',
            name='window',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

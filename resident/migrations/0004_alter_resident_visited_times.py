# Generated by Django 3.2.7 on 2023-10-13 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resident', '0003_resident_visited_times'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='visited_times',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
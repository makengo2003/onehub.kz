# Generated by Django 3.2.7 on 2023-09-02 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resident', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resident',
            name='locker',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

# Generated by Django 4.1.4 on 2022-12-13 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookingRequestNotificationEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='CarouselImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='carousel_images/')),
                ('serial_number', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceTypePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.PositiveIntegerField()),
                ('term', models.CharField(choices=[('hours', 'Час'), ('days', 'День'), ('weeks', 'Неделя'), ('months fix', 'Месяц Fix'), ('months flex', 'Месяц Flex')], max_length=50)),
                ('time_type', models.CharField(choices=[('nighttime', 'Ночь'), ('daytime', 'День'), ('day', 'Сутки'), ('anytime', 'Любое время')], max_length=50)),
                ('price', models.IntegerField()),
                ('place_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='site_settings.placetype')),
            ],
        ),
    ]

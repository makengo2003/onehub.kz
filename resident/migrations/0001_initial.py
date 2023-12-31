# Generated by Django 4.1.4 on 2022-12-13 13:21

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import project.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=255)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('profession', models.CharField(max_length=255)),
                ('starts_at', models.DateTimeField()),
                ('expires_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=project.utils.datetime_now, editable=False)),
                ('status', models.CharField(choices=[('active', 'Активный'), ('expired', 'Просрочен'), ('deleted', 'Не активный')], default='active', max_length=100)),
                ('used_discount', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('price', models.IntegerField()),
                ('payment_type', models.CharField(choices=[('cash', 'Наличные'), ('cashless', 'Безналичные'), ('barter', 'Бартер')], max_length=50)),
                ('place_number', models.CharField(blank=True, max_length=10, null=True)),
                ('place_type', models.CharField(max_length=100)),
                ('paper_count', models.IntegerField(blank=True, default=0, null=True)),
                ('duration', models.PositiveIntegerField()),
                ('term', models.CharField(choices=[('hours', 'Час'), ('days', 'День'), ('weeks', 'Неделя'), ('months fix', 'Месяц Fix'), ('months flex', 'Месяц Flex')], max_length=50)),
                ('time_type', models.CharField(choices=[('nighttime', 'Ночь'), ('daytime', 'День'), ('day', 'Сутки'), ('anytime', 'Любое время')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ResidentVisitedDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=project.utils.datetime_now)),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visited_days', to='resident.resident')),
            ],
        ),
    ]

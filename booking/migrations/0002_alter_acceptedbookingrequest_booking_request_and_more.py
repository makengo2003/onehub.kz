# Generated by Django 4.1.4 on 2023-01-15 11:24

from django.db import migrations, models
import django.db.models.deletion
import project.utils


class Migration(migrations.Migration):

    dependencies = [
        ('resident', '0001_initial'),
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptedbookingrequest',
            name='booking_request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='accepted_booking_request', to='booking.bookingrequest'),
        ),
        migrations.AlterField(
            model_name='bookingrequest',
            name='created_at',
            field=models.DateTimeField(default=project.utils.datetime_now),
        ),
        migrations.AlterField(
            model_name='frombookedplacetoresident',
            name='booked_place',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='from_booked_place_to_resident', to='booking.bookedplace'),
        ),
        migrations.AlterField(
            model_name='frombookedplacetoresident',
            name='resident',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='from_booked_place_to_resident', to='resident.resident'),
        ),
        migrations.AlterField(
            model_name='rejectedbookingrequest',
            name='booking_request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rejected_booking_request', to='booking.bookingrequest'),
        ),
    ]
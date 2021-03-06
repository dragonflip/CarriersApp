# Generated by Django 2.2.17 on 2021-01-26 21:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin-panel', '0005_auto_20210126_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='journey_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journeys', to='admin-panel.Journey'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 26, 23, 49, 32, 652905)),
        ),
    ]

# Generated by Django 2.2.17 on 2021-01-26 17:06

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin-panel', '0002_journey_station'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyerName', models.CharField(default='', max_length=50)),
                ('buyerSurname', models.CharField(default='', max_length=50)),
                ('price', models.FloatField(default='', max_length=10)),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 1, 26, 19, 6, 4, 864041))),
                ('type', models.CharField(choices=[('N', 'Normal'), ('K', 'Kids'), ('R', 'Retiree')], default='Normal', max_length=10)),
                ('journey', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='admin-panel.Journey')),
            ],
        ),
    ]

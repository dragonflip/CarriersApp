# Generated by Django 2.2.17 on 2021-01-26 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin-panel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default='', max_length=10)),
                ('fromWhere', models.CharField(default='', max_length=60)),
                ('whereTo', models.CharField(default='', max_length=60)),
                ('DepartureTime', models.TimeField(default='')),
                ('ArrivalTime', models.TimeField(default='')),
                ('FullDistance', models.FloatField(default='', max_length=10)),
                ('bus', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='admin-panel.Bus')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stationName', models.CharField(default='', max_length=60)),
                ('distanceFromStart', models.FloatField(default='', max_length=10)),
                ('stationArrivalTime', models.DateTimeField(default='')),
                ('stationDepartureTime', models.DateTimeField(default='')),
                ('journey', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='admin-panel.Journey')),
            ],
        ),
    ]

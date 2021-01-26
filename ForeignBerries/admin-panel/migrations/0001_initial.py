# Generated by Django 2.2.17 on 2021-01-26 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=60, null=True)),
                ('model', models.CharField(default='', max_length=50)),
                ('yearOfIssue', models.PositiveIntegerField(default='', max_length=10)),
                ('number', models.CharField(default='', max_length=10)),
                ('VinNumber', models.CharField(default='', max_length=10)),
                ('fuelConsumption', models.FloatField(default='', max_length=10, null=True)),
            ],
        ),
    ]

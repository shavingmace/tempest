# Generated by Django 4.1.3 on 2022-11-09 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tempest', '0004_weather_basedate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clothing_etc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
    ]
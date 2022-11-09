# Generated by Django 4.1.3 on 2022-11-09 06:13

from django.db import migrations, models
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tempest', '0002_clothing_bottom_clothing_outer_alter_weather_region_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weather',
            name='content',
        ),
        migrations.AddField(
            model_name='weather',
            name='baseTime',
            field=models.CharField(default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weather',
            name='json',
            field=jsonfield.fields.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='weather',
            name='region',
            field=models.CharField(max_length=10),
        ),
    ]
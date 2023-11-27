# Generated by Django 4.2.7 on 2023-11-20 09:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('back_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

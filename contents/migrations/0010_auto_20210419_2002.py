# Generated by Django 3.2 on 2021-04-19 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0009_auto_20210419_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='msg',
            field=models.CharField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='message',
            name='response',
            field=models.CharField(blank=True, max_length=5000),
        ),
    ]
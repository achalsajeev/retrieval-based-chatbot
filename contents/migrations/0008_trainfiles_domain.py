# Generated by Django 3.2 on 2021-04-19 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0007_auto_20210419_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainfiles',
            name='domain',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

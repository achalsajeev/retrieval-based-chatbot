# Generated by Django 3.2 on 2021-04-20 19:25

import contents.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0011_auto_20210420_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainfiles',
            name='trainfile',
            field=models.FileField(upload_to=contents.models.filepath),
        ),
    ]

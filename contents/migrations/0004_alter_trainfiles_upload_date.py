# Generated by Django 3.2 on 2021-04-16 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0003_trainfiles_upload_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainfiles',
            name='upload_date',
            field=models.DateField(blank=True),
        ),
    ]

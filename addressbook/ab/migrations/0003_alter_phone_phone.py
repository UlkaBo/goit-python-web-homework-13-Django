# Generated by Django 3.2.8 on 2021-10-15 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ab', '0002_auto_20211015_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]

# Generated by Django 2.1.7 on 2019-04-03 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_auto_20190403_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='displayPhoto',
            field=models.ImageField(blank=True, null=True, upload_to='item_pics'),
        ),
    ]

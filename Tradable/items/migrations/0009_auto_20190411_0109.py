# Generated by Django 2.1.7 on 2019-04-10 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0008_auto_20190403_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descriptionphoto',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.Item'),
        ),
    ]

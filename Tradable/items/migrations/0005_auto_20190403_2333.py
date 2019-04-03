# Generated by Django 2.1.7 on 2019-04-03 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20190403_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='condition',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10000, null=True),
        ),
    ]

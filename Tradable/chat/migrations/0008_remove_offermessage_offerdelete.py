# Generated by Django 2.1.7 on 2019-05-04 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_offermessage_offerdelete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offermessage',
            name='offerDelete',
        ),
    ]
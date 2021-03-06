# Generated by Django 2.1.7 on 2019-04-03 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_item_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescriptionPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='item_pics')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='displayPhoto',
            field=models.ImageField(null=True, upload_to='item_pics'),
        ),
        migrations.AddField(
            model_name='descriptionphoto',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='items.Item'),
        ),
    ]

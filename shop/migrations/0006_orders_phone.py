# Generated by Django 3.2.6 on 2021-12-15 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='phone',
            field=models.CharField(default='', max_length=111),
        ),
    ]

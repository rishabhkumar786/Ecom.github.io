# Generated by Django 3.2.6 on 2021-12-27 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_tilte_blogpost_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='thumbnail',
            field=models.ImageField(default='', upload_to='blog/images'),
        ),
    ]

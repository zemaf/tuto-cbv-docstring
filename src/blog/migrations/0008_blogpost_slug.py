# Generated by Django 3.1.6 on 2024-03-09 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20240309_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
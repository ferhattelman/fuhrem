# Generated by Django 4.1.3 on 2023-08-20 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_search_history_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='search_history',
            name='image_type',
            field=models.CharField(default='photo', max_length=15),
        ),
        migrations.AddField(
            model_name='search_history',
            name='search_amount',
            field=models.IntegerField(default=12),
        ),
    ]
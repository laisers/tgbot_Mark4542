# Generated by Django 3.2.6 on 2023-08-31 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0014_auto_20230831_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='vk_token',
            field=models.CharField(max_length=250, verbose_name='Token VK'),
        ),
    ]
# Generated by Django 3.2.6 on 2023-09-10 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0022_auto_20230910_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='google_token',
            field=models.CharField(max_length=250, verbose_name='Google токен'),
        ),
    ]

# Generated by Django 3.2.6 on 2023-08-23 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'QIWI', 'verbose_name_plural': 'QIWI'},
        ),
        migrations.AlterField(
            model_name='payment',
            name='shop',
            field=models.CharField(max_length=10, verbose_name='shop'),
        ),
    ]
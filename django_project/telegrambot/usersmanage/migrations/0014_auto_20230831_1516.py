# Generated by Django 3.2.6 on 2023-08-31 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0013_alter_templatesetting_watermark'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='vk_token',
            field=models.CharField(default=0, max_length=100, verbose_name='Token VK'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='templatesetting',
            name='main_template',
            field=models.ImageField(upload_to='Photos', verbose_name='Коллаж'),
        ),
        migrations.AlterField(
            model_name='templatesetting',
            name='watermark',
            field=models.ImageField(upload_to='Photos', verbose_name='Watermark'),
        ),
    ]

# Generated by Django 3.2.6 on 2023-08-23 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0003_auto_20230823_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='alltext',
            name='by_ref_text',
            field=models.TextField(default=0, help_text='"Текст рефералу" %link%', max_length=4024, verbose_name='Реф текст'),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.2.6 on 2023-08-27 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0008_alter_bot_damps_percentage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alltext',
            name='by_ref_text',
        ),
    ]

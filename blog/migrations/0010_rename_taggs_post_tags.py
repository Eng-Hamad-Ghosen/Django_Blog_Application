# Generated by Django 5.1.1 on 2024-09-21 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_rename_tags_post_taggs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='taggs',
            new_name='tags',
        ),
    ]

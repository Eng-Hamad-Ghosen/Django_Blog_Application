# Generated by Django 5.1.1 on 2024-09-21 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_post_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='tags',
            new_name='taggs',
        ),
    ]

# Generated by Django 4.0.4 on 2023-01-29 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0004_topic_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='abbr',
            field=models.CharField(default='', max_length=15, unique=True),
            preserve_default=False,
        ),
    ]

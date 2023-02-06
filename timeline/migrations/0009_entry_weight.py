# Generated by Django 4.1.5 on 2023-02-06 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0008_alter_topic_options_entry_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='weight',
            field=models.IntegerField(choices=[('-1', '-1'), ('0', '0'), ('1', '+1')], default='0', max_length=2),
        ),
    ]
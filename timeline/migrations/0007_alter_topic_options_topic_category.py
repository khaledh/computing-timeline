# Generated by Django 4.0.4 on 2023-01-30 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0006_alter_topic_abbr'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={},
        ),
        migrations.AddField(
            model_name='topic',
            name='category',
            field=models.CharField(choices=[('T', 'Topic'), ('P', 'Person'), ('O', 'Organization')], default='T', max_length=2),
        ),
    ]

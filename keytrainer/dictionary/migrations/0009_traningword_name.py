# Generated by Django 2.2.2 on 2019-07-06 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0008_remove_word_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='traningword',
            name='name',
            field=models.CharField(default='aaa', max_length=32),
            preserve_default=False,
        ),
    ]
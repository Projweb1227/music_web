# Generated by Django 4.1.5 on 2023-05-19 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_app', '0006_alter_song_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='slug',
            field=models.SlugField(max_length=100, null=True, unique=True),
        ),
    ]
# Generated by Django 4.1.5 on 2023-05-19 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_app', '0009_alter_album_author_alter_musicalgenre_genre_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='audio_link',
        ),
    ]

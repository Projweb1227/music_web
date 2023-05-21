from django.db import models
from datetime import date
from django.urls import reverse
import os
from django.conf import settings


class Author(models.Model):
    name = models.TextField()
    # songs = models.ManyToManyField("Song", related_name="authors")

    def __str__(self):
        return self.name
    



class Album(models.Model):
    title = models.TextField()
    author = models.ForeignKey(
        Author, on_delete=models.PROTECT, related_name="albums", blank=False
    )
    # songs = models.ManyToManyField("Song", related_name="albums")

    def __str__(self):
        return self.title


class MusicalGenre(models.Model):
    genre = models.TextField(default="Other")

    def __str__(self):
        return self.genre


class Playlist(models.Model):
    name = models.TextField()
    songs = models.ManyToManyField("Song")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

def song_file_path(instance, filename):
    # Obtiene la ruta completa hacia la carpeta "songs_save" en tu proyecto Django
    base_path = os.path.join(settings.MEDIA_ROOT, 'songs_save')

    # Genera la ruta de almacenamiento del archivo dentro de la carpeta "songs_save"
    # en función del nombre del archivo y el ID de la instancia
    return os.path.join(base_path, str(instance.pk), filename)

class Song(models.Model):
    name = models.TextField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="songs")
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="songs",
        null=True,
        blank=True,
    )
    musicalGenre = models.ForeignKey(
        MusicalGenre,
        on_delete=models.CASCADE,
        related_name="songs",
        null=True,
        blank=True,
    )
    image = models.ImageField(null=True, blank=True)
    audio_file = models.FileField(upload_to=song_file_path, blank=True, null=False, default="")
    duration = models.CharField(max_length=10, null=True, blank=True, default="-")
    date = models.DateField(default=date.today)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Song edited
        if self.pk:
            old_song = Song.objects.get(pk=self.pk)
            old_author = old_song.author
            # If author is changed, remove song
            if old_author != self.author:
                old_author.songs.remove(self)

        super().save(*args, **kwargs)

        if self.author:
            self.author.songs.add(self)

    def get_absolute_url(self):
        return reverse("songs:song_details", kwargs={"pk": self.pk})
        # return reverse("playlist")

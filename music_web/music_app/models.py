from django.db import models
from datetime import date
from django.urls import reverse


class MusicalGenre(models.Model):
    genre = models.TextField()

    def __str__(self):
        return self.genre


class Song(models.Model):
    name = models.TextField(max_length=100)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    album = models.ForeignKey("Album", on_delete=models.CASCADE, null=True, blank=True)
    musicalGenre = models.ForeignKey(
        MusicalGenre, on_delete=models.CASCADE, null=True, blank=True
    )
    image = models.ImageField(null=True, blank=True)
    audio_file = models.FileField(blank=True, null=True)
    audio_link = models.CharField(max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateField(default=date.today)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("playlist")


class Album(models.Model):
    title = models.TextField()
    author = models.ForeignKey("Author", on_delete=models.PROTECT, blank=False)
    songs = models.ManyToManyField("Song", related_name="albums")


class Author(models.Model):
    # removed musicalGenre
    name = models.TextField()
    songs = models.ManyToManyField("Song", related_name="authors")

    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.TextField()
    songs = models.ManyToManyField(Song)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

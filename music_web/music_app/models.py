from django.db import models

class MusicalGenre(models.Model):
    genre = models.TextField()

    class Meta:
        ordering = ['genre']

    def __str__(self):
        return self.genre


class Album(models.Model):
    title = models.TextField()
    author = models.ForeignKey('Author', on_delete=models.PROTECT, blank=False)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.TextField()
    musicalGenre = models.ForeignKey(MusicalGenre, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.TextField()
    musicalGenre = models.ForeignKey(MusicalGenre, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField()
    image = models.ImageField()
    audio_file = models.FileField(blank=True, null=True)
    audio_link = models.CharField(max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=10)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.TextField()
    songs = models.ManyToManyField(Song)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
        
        
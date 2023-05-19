from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from music_app.models import Song, Author, Album, MusicalGenre


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class SongForm(ModelForm):
    song_name = forms.CharField(label="Song Tittle", max_length=100)
    author_name = forms.CharField(label="Author", max_length=100)
    album_name = forms.CharField(label="Album", max_length=100)
    musical_genre_name = forms.CharField(label="Music Genere", max_length=100)

    class Meta:
        model = Song
        fields = ["song_name", "author_name", "album_name", "musical_genre_name"]
        # exclude = ("author","date", "audio_file")

    def checkAuthorExists(self):
        author_name = self.cleaned_data["author_name"]
        try:
            author = Author.objects.get(name=author_name)
        except Author.DoesNotExist:
            author = Author.objects.create(name=author_name)

        return author

    def checkMusicalGenereExists(self, musical_genre_name):
        try:
            musical_genre = MusicalGenre.objects.get(genre=musical_genre_name)
        except MusicalGenre.DoesNotExist:
            musical_genre = MusicalGenre.objects.create(genre=musical_genre_name)

        return musical_genre

    def checkAlbumExists(self, album_name, author):
        try:
            album = Album.objects.get(title=album_name, author=author)
        except:
            album = Album.objects.create(title=album_name, author=author)
        return album

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = self.cleaned_data["song_name"]
        instance.author = self.checkAuthorExists()

        album_name = self.cleaned_data["album_name"]
        if album_name:
            instance.album = self.checkAlbumExists(album_name, instance.author)

        musical_genre_name = self.cleaned_data["musical_genre_name"]
        if musical_genre_name:
            instance.musicalGenre = self.checkMusicalGenereExists(musical_genre_name)
        if commit:
            instance.save()
        return instance

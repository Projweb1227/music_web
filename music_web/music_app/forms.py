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


from django import forms
from .models import Song, MusicalGenre, Album, Author

class SongForm(forms.ModelForm):
    musical_genre_name = forms.ModelChoiceField(
        queryset=MusicalGenre.objects.all(),
        label="Genre",
        required=False,
        empty_label="Select an existing genre",
        widget=forms.Select(attrs={"class": "custom-class"}),
    )
    author_name = forms.CharField(label="Author", max_length=100, required=True)
    album_name = forms.CharField(label="Album", max_length=100, required=False)
    audio_file = forms.FileField(label="Audio File", required=False)

    class Meta:
        model = Song
        fields = [
            "name",
            "author_name",
            "album_name",
            "musical_genre_name",
            "audio_file",
        ]
        labels = {"name": "Title"}
        widgets = {
            "name": forms.TextInput(),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        author_name = self.cleaned_data.get("author_name")
        instance.author, _ = Author.objects.get_or_create(name=author_name)

        album_name = self.cleaned_data.get("album_name")
        if album_name:
            instance.album, _ = Album.objects.get_or_create(
                title=album_name, author=instance.author
            )

        musical_genre_name = self.cleaned_data["musical_genre_name"]
        if musical_genre_name:
            instance.musicalGenre, _ = MusicalGenre.objects.get_or_create(
                genre=musical_genre_name
            )
        else:
            instance.musicalGenre, _ = MusicalGenre.objects.get_or_create(genre="Other")

        if commit:
            instance.save()
        return instance



class EditSongForm(forms.ModelForm):
    musical_genre = forms.ModelChoiceField(
        queryset=MusicalGenre.objects.all(),
        label="Genre",
        required=False,
        empty_label="Select an existing genre",
        widget=forms.Select(attrs={"class": "custom-class"}),
    )
    author_new = forms.CharField(label="Author", max_length=100, required=True)
    album_new = forms.CharField(label="Album", max_length=100, required=False)
    audio_file = forms.FileField(label="Audio File", required=False)  # Added field for editing audio_file

    class Meta:
        model = Song
        fields = [
            "name",
            "author_new",
            "album_new",
            "musical_genre",
            "audio_file",  # Added audio_file field to the form
        ]
        labels = {"name": "Title"}
        widgets = {
            "name": forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["author_new"].initial = self.instance.author.name

        # Album known
        if self.instance.album:
            self.fields["album_new"].initial = self.instance.album.title
        self.fields["musical_genre"].initial = self.instance.musicalGenre

    def save(self, commit=True):
        instance = super().save(commit=False)
        author_new = self.cleaned_data.get("author_new")
        album_new = self.cleaned_data.get("album_new")

        author, _ = Author.objects.get_or_create(name=author_new)
        instance.author = author

        if album_new:
            album, _ = Album.objects.get_or_create(title=album_new)
            instance.album = album

        # Check if a new audio file was provided
        audio_file = self.cleaned_data.get("audio_file")
        if audio_file:
            instance.audio_file = audio_file

        if commit:
            instance.save()
        return instance


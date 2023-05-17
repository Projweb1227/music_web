
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required


def user_is_authenticated(user):
    return user.is_authenticated



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})



@user_passes_test(user_is_authenticated, login_url='register')
def home(request):
        songs = Song.objects.all()
        playlists = Playlist.objects.all()
        albums = Album.objects.all()
        authors = Author.objects.all()
        musicalgenres = MusicalGenre.objects.all()
        return render(request, "web/index.html", {'songs': songs, 'playlists': playlists, 'albums': albums, 'authors': authors, 'musicalgenres': musicalgenres})


def playlist(request):
    author_id = request.GET.get('author_id')
    if author_id:
        songs = Song.objects.filter(author=author_id).order_by('name')
    else:
        songs = Song.objects.all().order_by('name')
    return render(request, 'web/playlist.html', {'songs': songs})


def song(request, name):
    song = get_object_or_404(Song, name=name)
    context = {'song': song}
    return render(request, 'web/song.html', context)

def play_song(request, name):
    song = get_object_or_404(Song, name=name)
    file_url = song.audio_link or song.audio_file.url
    response = HttpResponse()
    response['Content-Type'] = 'audio/mpeg'
    response['Content-Length'] = song.audio_file.size
    response['Content-Disposition'] = 'attachment; filename=%s' % song.audio_file.name
    response.write(song.audio_file.read())
    return response


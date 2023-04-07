
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import UserRegistrationForm  



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



def song(request, song_id):
        try:
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
                raise HttpResponse("Aquesta canço no existeix")
        return render(request, 'web/song.html', {'song': song})



def album_list(request):
    albums = Album.objects.order_by('musicalGenre__genre', 'title')
    return render(request, 'web/album_list.html', {'albums': albums})




def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

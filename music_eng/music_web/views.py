from django.shortcuts import render
from django.http import HttpResponse
from web.models import Song, Playlist, Album, Author, DatePublication, MusicalGenre
from django.views import generic

def home(request):
        songs = Song.objects.all()
        playlists = Playlist.objects.all()
        albums = Album.objects.all()
        authors = Author.objects.all()
        musicalgenres = MusicalGenre.objects.all()
        return render(request, "web/index.html", {'songs': songs, 'playlists': playlists, 'albums': albums, 'authors': authors, 'musicalgenres': musicalgenres})

def song(request, song_id):
        try:
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
                raise Http404("Aquesta canço no existeix")
        return render(request, 'web/song.html', {'song': song})

class DatePublicationView(generic.DetailView):
       model = DatePublication
       template_name = 'web/datepublication.html'
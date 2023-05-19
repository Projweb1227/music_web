import vlc
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from .models import *
from django.views import View
from .forms import UserCreationForm, SongForm, EditSongForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import DetailView

from django.http import HttpResponse


# Authocompletion
from django.http import JsonResponse
from django.views.decorators.http import require_GET


#Login
class LoginPageView(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('playlist')

        return render(request, 'registration/login.html', {'error': 'Invalid credentials'})

class SignUpPageView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('playlist')
        return render(request, 'registration/register.html', {'form': form})



class HomeView:
    template_name = "base.html"


def home(request):
    return render(request, "base.html")


def playlist(request):
    author_id = request.GET.get("author_id")
    if author_id:
        songs = Song.objects.filter(author=author_id).order_by("name")
    else:
        songs = Song.objects.all().order_by("name")
    return render(request, "web/playlist.html", {"songs": songs})


def song_list(request):
    songs = Song.objects.all()
    return render(request, "song_list.html", {"songs": songs})


def play_song(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        return HttpResponse("Song not found")

    if song.audio_file:
        player = vlc.MediaPlayer(song.audio_file.path)
        player.play()

    return render(request, "play_song.html", {"song": song})


def edit_song(request, pk):
    song = get_object_or_404(Song, pk=pk)

    if request.method == "POST":
        form = EditSongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect("songs:song_details", pk=song.pk)
    else:
        form = EditSongForm(instance=song)

    return render(request, "songs/edit.html", {"form": form})




# HTML views
class SongCreate(CreateView):
    model = Song
    template_name = "songs/form.html"
    form_class = SongForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SongCreate, self).form_valid(form)


class SongDetail(DetailView):
    model = Song
    template_name = "songs/details.html"
    context_object_name = "song"

    def get_context_data(self, **kwargs):
        context = super(SongDetail, self).get_context_data(**kwargs)
        return context


# Autocomplete
@require_GET
def author_suggestions(request):
    term = request.GET.get("term")
    suggestions = Author.objects.filter(name__icontains=term).values_list(
        "name", flat=True
    )
    return JsonResponse(list(suggestions), safe=False)


@require_GET
def album_suggestions(request):
    term = request.GET.get("term")
    suggestions = Album.objects.filter(title__icontains=term).values_list(
        "title", flat=True
    )
    return JsonResponse(list(suggestions), safe=False)

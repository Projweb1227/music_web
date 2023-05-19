from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .models import *
from django.views import generic
from .forms import UserRegistrationForm, SongForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render


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


# HTML views
class SongCreate(CreateView):
    model = Song
    template_name = "songs/form.html"
    form_class = SongForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SongCreate, self).form_valid(form)

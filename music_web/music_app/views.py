
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin





class HomeView:
    template_name = 'base.html'


def home(request):
    return render(request, 'base.html')


def playlist(request):
    author_id = request.GET.get('author_id')
    if author_id:
        songs = Song.objects.filter(author=author_id).order_by('name')
    else:
        songs = Song.objects.all().order_by('name')
    return render(request, 'web/playlist.html', {'songs': songs})


def song_list(request):
    songs = Song.objects.all()
    return render(request, 'song_list.html', {'songs': songs})






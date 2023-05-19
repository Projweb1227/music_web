from django.urls import path
from music_app.forms import SongForm
from django.views.generic.edit import CreateView
from music_app.models import Song
from music_app import views

app_name = "songs"

urlpatterns = [
    path("", views.song_list, name="song_list"),
    path(
        "create",
        views.SongCreate.as_view(),
        name="song_create",
    ),
    path("song/<int:pk>", views.SongDetail.as_view(), name="song_details"),
    path('edit/<int:pk>', views.edit_song, name='edit_song'),


    #Autocompletion
    path("author-suggestions/", views.author_suggestions, name="author_suggestions"),
    path("album-suggestions/", views.album_suggestions, name="album_suggestions"),
]

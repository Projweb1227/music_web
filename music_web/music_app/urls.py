from django.urls import path
from music_app.forms import SongForm
from django.views.generic.edit import CreateView
from music_app.models import Song
from music_app.views import SongCreate, song_list

app_name = "songs"

urlpatterns = [
    path("", song_list, name="song_list"),
    path(
        "create",
        SongCreate.as_view(),
        name="song_create",
    ),
]

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Author)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(Album)
admin.site.register(MusicalGenre)



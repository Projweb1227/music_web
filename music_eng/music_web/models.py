from django.db import models

class Song(models.Model):
    name = models.CharField(max_length=256, blank=False, unique=True)
    musicalGenre = models.ForeignKey(MusicalGenre, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.PROTECT, blank=False)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self) -> str:
        return self.name



class Playlist(models.Model):
    name = models.CharField(max_length=256)
    song = models.ManyToManyField(Song)

    class Meta:
        ordering = ['name']
        
    def __str__(self) -> str:
            return self.name
            
           
           
class Album(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, blank=False)
    
    def __str__(self):
        return self.title

           
class Author(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    song = models.ManyToManyField(Song)
    musicalGenre = models.ForeignKey(MusicalGenre, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
        
              
              
class DatePublication(models.Model):
    date = models.DateField()
    song = models.ManyToManyField(Song)
    author = models.ManyToManyField(Author)
    musicalGenre = models.ForeignKey(MusicalGenre, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.date
        
        
        
class MusicalGenre(models.Model):
    genre = models.CharField(max_length=30)
    
    class Meta:
        ordering = ['genre']

    def __str__(self):
        return self.genre
        
        
        
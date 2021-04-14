from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Songs(models.Model):
    artist_name = models.TextField(max_length=200)
    Song_name = models.TextField(max_length=200)
    album_name = models.TextField(max_length=200)
    track_number =  models.TextField(max_length=100)
    release_date = models.TextField(max_length=100)
    popularity = models.IntegerField(default=0)
    songs_id = models.TextField(max_length=100, db_index=True)
    Song_image = models.TextField(max_length=500)
    Song_preview = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    likes = models.ManyToManyField(User, related_name='songs_post')

    def total_likes(self):
        return self.likes.count()

    


class Sentiment_Records(models.Model):
    song_comments = models.TextField(max_length=500)
    sentiment_result = models.TextField(max_length=200)
    sentiment_polarity = models.FloatField(validators=[MinValueValidator(-1), MaxValueValidator(1)])
    sentiment_subjectivity = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    usr = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    song = models.ForeignKey(Songs, null=True, on_delete=models.SET_NULL)

    def __str__ (self):
        return self.song_comments
 

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Songs(models.Model):
    artist_name = models.TextField(max_length=200)
    Song_name = models.TextField(max_length=200)
    album_name = models.TextField(max_length=200)
    track_number =  models.TextField(max_length=100)
    release_date = models.TextField(max_length=100)
    popularity = models.TextField(max_length=100)
    songs_id = models.TextField(max_length=100)
    Song_image = models.TextField(max_length=500)
    Song_preview = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


class Sentiment_Records(models.Model):
    song_comments = models.TextField(max_length=500)
    sentiment_result = models.TextField(max_length=200)
    sentiment_polarity = models.TextField(max_length=200)
    sentiment_subjectivity = models.TextField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    usr = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    song = models.ForeignKey(Songs, null=True, on_delete=models.SET_NULL)
 
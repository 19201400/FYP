from django.contrib import admin
from .models import *
# Register your models here.

class SongsAdmin (admin.ModelAdmin):
	list_display = ('id', 'artist_name', 'Song_name', 'album_name', 'track_number', 'release_date', 'popularity', 'songs_id', 'Song_image', 'Song_preview', 'date_created')

class Sentiment_RecordsAdmin(admin.ModelAdmin):
	list_display = ('id', 'song_comments', 'sentiment_result', 'sentiment_polarity', 'sentiment_subjectivity', 'date_created', 'usr', 'song')

admin.site.register(Songs, SongsAdmin)
admin.site.register(Sentiment_Records, Sentiment_RecordsAdmin)
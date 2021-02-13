from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *

from django.contrib import messages

from accounts.models import *
from django.db.models import Q

from .decorators import unauthenticated_user, allowed_users, admin_only

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk


# Try to restrict the user go to index page whithout logged in...
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def AdminHomepage(request):

	users  = User.objects.all()
	comments = Sentiment_Records.objects.all()
	groups = Group.objects.all()

	total_users = users.count()
	total_comments = comments.count()

	context = {'users':users, 'comments':comments, 'groups':groups, 'total_users':total_users, 'total_comments':total_comments}
	return render(request, 'accounts/dashboard.html', context)




@unauthenticated_user
def registerPage(request):
	form = UserCreationForm()

	# Check the user whether registered... If yes redirect to login page...
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer') 
			user.groups.add(group)

			messages.success(request, 'Hi,' + username)
			messages.success(request, 'Your account was created! Please login to your portal')
			return redirect('login')
	context = {'form':form}
	return render(request, 'accounts/register.html', context)





# Logout the user...
def logoutUser(request):
	logout(request)
	return redirect('login')







@unauthenticated_user
def loginPage(request):
	
		# Check the user whether signed in... If yes redirect to login page...
		if request.method == "POST":
			username = request.POST.get('username')
			password = request.POST.get('password')
			usr = authenticate(request, username=username, password=password)
			if usr is not None:
				login(request, usr)
				return redirect('music')
			else:
				messages.info(request, 'Username Or Password incorrect!')
				messages.info(request, 'Please try again!!')
				
		context = {}
		return render(request, 'accounts/login.html', context)







@login_required(login_url='login')
def musicPage(request):	
	if request.method=='POST':
		artist = request.POST.get('artist')

		# Connecting to the Spotify Server...
		spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='c233c239c8594b0791a72936914e9d01',client_secret='a8bf49cc1d0c48758c9e6f6081d7eeb8',))
		# Search for the artist name...
		result = spotify.search(artist)
		# Get the artist uri for Spotify...
		artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
		# Get top ten songs for the specific artist...
		results = spotify.artist_top_tracks(artist_uri)
		final_result=results['tracks'][:10]

		# Loop the tracks information from Spotify...
		for x in final_result:
			artistName = x['artists'][0]['name']
			songName = x["name"]
			albumName = x["album"]["name"]
			trackNumber = str(x["track_number"])
			releaseDate = x["album"]["release_date"]
			popularity = x["popularity"]
			songID = str(x["id"])

			SongImage = x["album"]["images"][0]["url"]
			songPreview = str(x["preview_url"])

			# Save songs information to Django database from Spotify...
			store_obj = Songs(artist_name = artistName, Song_name = songName, album_name = albumName, track_number = trackNumber, release_date = releaseDate, popularity = popularity, songs_id = songID, Song_image = SongImage, Song_preview = songPreview)
			store_obj.save()	

		songs = Songs.objects.filter(Q(artist_name__contains=artist) | Q(Song_name__contains=artist) | Q(album_name__contains=artist))
		
		return render(request, 'accounts/music.html', {'db_results':songs})

	else:
		default_songs = Songs.objects.filter(popularity__gte=70)

		return render(request, 'accounts/music.html', {'filter_results':default_songs})

@login_required(login_url='login')
def music_profilePage(request, song_id):

	song = Songs.objects.get(id=song_id)
	comments = Sentiment_Records.objects.filter(song__exact=song)
	context = {'song':song, 'comments':comments}

	if request.method=='POST':
		sentiment_result = ""

		song_Comments = request.POST.get('song_comments')

		result = TextBlob(song_Comments)

		# polarity is between -1 to 1, where -1 is negative and 1 is positive
		polarity = result.sentiment[0]
		# subjectivity is between 0 to 1, where 0 is objective and 1 is subjective
		subjectivity = result.sentiment[1]

		print("Polarity = " + str(polarity), "Subjectivity = " + str(subjectivity))

		if polarity < 0:
			sentiment_result = "Negative"
			print(sentiment_result)
			#return render(request, 'accounts/negative.html')
			
		elif polarity == 0:
			sentiment_result = "Neutral"
			print(sentiment_result)
			#return render(request, 'accounts/neutral.html')
			
		elif polarity > 0:
			sentiment_result = "Postive"
			print(sentiment_result)
			#return render(request, 'accounts/positive.html')
			

		# Save the users comments with sentiment records to db...
		store_comments_obj = Sentiment_Records(song_comments = song_Comments, sentiment_result = sentiment_result, sentiment_polarity = polarity, sentiment_subjectivity = subjectivity, usr = request.user, song = song)
		store_comments_obj.save()


	return render(request, 'accounts/music_profile.html', context)





@login_required(login_url='login')
def RecommendationPage(request):
	return render(request, 'accounts/recommendation.html')

@login_required(login_url='login')
def recordsPage(request):

	positive_count = Sentiment_Records.objects.filter(Q(sentiment_result__exact="Postive") & Q(usr__exact=request.user)).count()
	negative_count = Sentiment_Records.objects.filter(Q(sentiment_result__exact="Negative") & Q(usr__exact=request.user)).count()
	neutral_count = Sentiment_Records.objects.filter(Q(sentiment_result__exact="Neutral") & Q(usr__exact=request.user)).count()

	specific_comments = Sentiment_Records.objects.filter(usr__exact=request.user)

	context = {'positive_count':positive_count, 'negative_count':negative_count, 'neutral_count':neutral_count , 'specific_comments':specific_comments}
	return render(request, 'accounts/records.html', context)

@login_required(login_url='login')
def notificationPage(request):
	return render(request, 'accounts/404.html')


@login_required(login_url='login')
def positivePage(request):
	return render(request, 'accounts/positive.html')


@login_required(login_url='login')
def neutralPage(request):
	return render(request, 'accounts/neutral.html')


@login_required(login_url='login')
def nagativePage(request):
	return render(request, 'accounts/nagative.html')




















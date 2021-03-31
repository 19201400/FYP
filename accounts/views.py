from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse 

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *

from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.models import *
from django.db.models import Q

from .decorators import unauthenticated_user, allowed_users, admin_only
from .filters import commentsFilters
from .forms import CreateUserForm

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk












def LikeView(request, pk):
	s = get_object_or_404(Songs, id=request.POST.get('song.id'))
	liked = False 
	if s.likes.filter(id=request.user.id).exists():
		s.likes.remove(request.user)
		liked = False
	else:
		s.likes.add(request.user)
		liked = True
	return HttpResponseRedirect(reverse('music_profile', args=[str(pk)]))
















# Try to restrict the user go to index page whithout logged in...
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def AdminHomepage(request):

	users  = User.objects.all()
	paginator2 = Paginator(users, 4)
	page_number2 = request.GET.get('page2')
	page_obj2 = paginator2.get_page(page_number2)

	comments = Sentiment_Records.objects.all()
	paginator = Paginator(comments, 4)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	groups = Group.objects.all()

	total_users = users.count()
	total_comments = comments.count()

	context = {'users':page_obj2, 'comments':page_obj, 'groups':groups, 'total_users':total_users, 'total_comments':total_comments}
	return render(request, 'accounts/dashboard.html', context)














@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()

	# Check the user whether registered... If yes redirect to login page...
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
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

			# Query of the song_id.
			# Separate store the Spotify values
			artistName = x['artists'][0]['name']
			songName = x["name"]
			albumName = x["album"]["name"]
			trackNumber = str(x["track_number"])
			releaseDate = x["album"]["release_date"]
			popularity = x["popularity"]
			songID = str(x["id"])

			SongImage = x["album"]["images"][0]["url"]
			songPreview = str(x["preview_url"])

			check_duplicate = Songs.objects.filter(Q(songs_id__exact=str(x["id"])))

			if len(check_duplicate) == 0:

				# Save songs information to Django database from Spotify...
				store_obj = Songs(artist_name = artistName, Song_name = songName, album_name = albumName, track_number = trackNumber, release_date = releaseDate, popularity = popularity, songs_id = songID, Song_image = SongImage, Song_preview = songPreview)
				store_obj.save()	

		songs = Songs.objects.filter(Q(artist_name__contains=artist) | Q(Song_name__contains=artist) | Q(album_name__contains=artist))

		return render(request, 'accounts/music.html', {'db_results':songs})

	else:
		# Queryset of all distinct artists...
		cat = Songs.objects.values('artist_name').order_by('artist_name').distinct()

		# Show the songs with upper then 70 popularity...
		default_songs = Songs.objects.filter(popularity__gte=70)

		# Pagination...
		paginator = Paginator(default_songs, 12)
		page = request.GET.get('page')
		try:
			songs = paginator.page(page)
		except PageNotAnInteger:
			songs = paginator.page(1)
		except EmptyPage:
			songs = paginator.page(paginator.num_pages)

		return render(request, 'accounts/music.html', {'filter_results':songs, 'cat':cat})















@login_required(login_url='login')
def music_profilePage(request, song_id):

	song = Songs.objects.get(id=song_id)
	comments = Sentiment_Records.objects.filter(song__exact=song)

	# Get the total likes on the specific song
	stuff = get_object_or_404(Songs, id=song_id)
	total_likes = stuff.total_likes()

	liked = False
	if stuff.likes.filter(id=request.user.id).exists():
		liked = True

	context = {'song':song, 'comments':comments, 'total_likes':total_likes, 'liked':liked}

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

			# Save the users comments with sentiment records to db...
			store_comments_obj = Sentiment_Records(song_comments = song_Comments, sentiment_result = sentiment_result, sentiment_polarity = polarity, sentiment_subjectivity = subjectivity, usr = request.user, song = song)
			store_comments_obj.save()
			return HttpResponse("<br><br><br><br><br><br><center><h1>Thanks for your feedback<br>Your Mood is <font color='red'>NEGATIVE!</font></h1></center>")
			
		elif polarity == 0:
			sentiment_result = "Neutral"
			print(sentiment_result)

			# Save the users comments with sentiment records to db...
			store_comments_obj = Sentiment_Records(song_comments = song_Comments, sentiment_result = sentiment_result, sentiment_polarity = polarity, sentiment_subjectivity = subjectivity, usr = request.user, song = song)
			store_comments_obj.save()
			return HttpResponse("<br><br><br><br><br><br><center><h1>Thanks for your feedback<br>Your Mood is <font color='orange'>NEUTRAL!</font></h1></center>")
			
		elif polarity > 0:
			sentiment_result = "Positive"
			print(sentiment_result)

			# Save the users comments with sentiment records to db...
			store_comments_obj = Sentiment_Records(song_comments = song_Comments, sentiment_result = sentiment_result, sentiment_polarity = polarity, sentiment_subjectivity = subjectivity, usr = request.user, song = song)
			store_comments_obj.save()
			return HttpResponse("<br><br><br><br><br><br><center><h1>Thanks for your feedback<br>Your Mood is <font color='green'>POSITIVE!</font></h1></center>")
		
	return render(request, 'accounts/music_profile.html', context)












@login_required(login_url='login')
def RecommendationPage(request):

	just_updated_song = Songs.objects.filter(Q(release_date__icontains="2021") | Q(release_date__icontains="2020"))
	# Pagination...
	paginator1 = Paginator(just_updated_song, 8)
	page = request.GET.get('page')
	try:
		songs1 = paginator1.page(page)
	except PageNotAnInteger:
		songs1 = paginator1.page(1)
	except EmptyPage:
		songs1 = paginator1.page(paginator1.num_pages)



	sounds_of_7080s = Songs.objects.filter(Q(release_date__icontains="197") | Q(release_date__icontains="198"))
	# Pagination...
	paginator2 = Paginator(sounds_of_7080s, 8)
	page = request.GET.get('page2')
	try:
		songs2 = paginator2.page(page)
	except PageNotAnInteger:
		songs2 = paginator2.page(1)
	except EmptyPage:
		songs2 = paginator2.page(paginator2.num_pages)


	others_liked_songs = Sentiment_Records.objects.filter(Q(sentiment_result__exact="Positive") & ~Q(usr__exact=request.user))
	# Pagination...
	paginator3 = Paginator(others_liked_songs, 8)
	page = request.GET.get('page3')
	try:
		songs3 = paginator3.page(page)
	except PageNotAnInteger:
		songs3 = paginator3.page(1)
	except EmptyPage:
		songs3 = paginator3.page(paginator3.num_pages)

	positive_comm = Sentiment_Records.objects.filter(Q(sentiment_result__exact="Positive") & Q(usr__exact=request.user))[:8]
 
	context = {'positive_comm':positive_comm, 'just_updated_song':songs1, 'sounds_of_7080s':songs2, 'others_liked_songs':songs3}

	return render(request, 'accounts/recommendation.html', context)













@login_required(login_url='login')
def recordsPage(request):

	positive_count = Sentiment_Records.objects.filter(Q(sentiment_result__exact="Positive") & Q(usr__exact=request.user)).count()
	negative_count = Sentiment_Records.objects.filter(Q(sentiment_result__exact="Negative") & Q(usr__exact=request.user)).count()
	neutral_count = Sentiment_Records.objects.filter(Q(sentiment_result__exact="Neutral") & Q(usr__exact=request.user)).count()

	specific_comments = Sentiment_Records.objects.filter(usr__exact=request.user)

	comment_filters = commentsFilters(request.GET, queryset=specific_comments)
	specific_comments = comment_filters.qs

	context = {'positive_count':positive_count, 'negative_count':negative_count, 'neutral_count':neutral_count , 'specific_comments':specific_comments, 'comment_filters':comment_filters}
	return render(request, 'accounts/records.html', context)






















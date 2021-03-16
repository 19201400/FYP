from django.urls import path
from . import views

urlpatterns = [
    path('', views.musicPage, name = "music"),

    path('dashboard/', views.AdminHomepage, name = "dashboard"),


    path('register/', views.registerPage, name = "register"),

    path('login/', views.loginPage, name = "login"), 

    path('logout/', views.logoutUser, name = "logout"),


    path('music/', views.musicPage, name = "music"),

    path('music_profile/<int:song_id>/', views.music_profilePage, name = "music_profile"),
    path('like/<int:pk>/', views.LikeView, name="like_post"),


    path('recommendation/', views.RecommendationPage, name = "recommendation"),

    path('records/', views.recordsPage, name = "records"),

]

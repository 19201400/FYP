from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

from .views import UserEditView, PasswordsChangeView

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

    path('delete_record/<str:pk>/', views.deleteRecord, name = "delete_record"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),

    path('edit_profile/', UserEditView.as_view(), name="edit_profile"),

    path('password/', PasswordsChangeView.as_view(template_name="accounts/password_change.html")),



]

from django.contrib import admin
from django.urls import path
from web.views import main_view, registration_view, auth_view, profile_view, logout_view, welcome_view, \
    delete_profile_view, analyze_view, histogram_view

urlpatterns = [
    path('main', main_view, name="main"),
    path('registration/', registration_view, name="registration"),
    path('auth/', auth_view, name="auth"),
    path('profile/', profile_view, name="profile"),
    path('logout/', logout_view, name="logout"),
    path('welcome/', welcome_view, name="welcome"),
    path('delete_profile/', delete_profile_view, name="delete_profile"),
    path('analyze/', analyze_view, name="analyze_view"),
    path('histogram/', histogram_view, name="histogram_view")
]
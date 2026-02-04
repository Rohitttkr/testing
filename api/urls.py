from django.urls import path
from .views import get_song_link

urlpatterns = [
    path('search/', get_song_link, name='search_song'),
]
from django.urls import path
from .views import get_song_link  # Views file se function ko import kiya

urlpatterns = [
    # Jab koi 'https://tumhara-app.onrender.com/api/search/' par request bhejega
    # toh ye niche wala path trigger hoga aur get_song_link function chalega.
    
    path('search/', get_song_link, name='get_song_link'),
]

from django.shortcuts import render

# Create your views here.
import yt_dlp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def get_audio_info(song_name):
    # yt-dlp configurations
ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch1',
    'noplaylist': True,
    'nocheckcertificate': True,
    # Ye headers add karne se YouTube ko lagega browser se request aa rahi hai
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song_name, download=False)
            if 'entries' in info:
                video = info['entries'][0]
            else:
                video = info
                
            return {
                "title": video.get('title'),
                "url": video.get('url'),
                "thumbnail": video.get('thumbnail'),
                "duration": video.get('duration')
            }
    except Exception as e:
        print(f"Error: {e}")
        return None

@api_view(['POST'])
def get_song_link(request):
    # User se song_name lena
    song_name = request.data.get('song_name')
    
    if not song_name:
        return Response({"error": "song_name is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    data = get_audio_info(song_name)
    
    if data:
        return Response(data, status=status.HTTP_200_OK)
    return Response({# views.py mein jahan except hai wahan ye likho
except Exception as e:
    print(f"DEBUG ERROR: {str(e)}") # Ye Render logs mein dikhega
    return None}, status=status.HTTP_404_NOT_FOUND)

import os
import yt_dlp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def get_audio_info(song_name):
    # Cookies file ka path (jahan manage.py hai)
    cookie_path = os.path.join(os.getcwd(), 'cookies.txt')

    ydl_opts = {
        # 'bestaudio/best' ki jagah ye format string use karein
        'format': 'bestaudio/best[ext=m4a]/best[ext=mp3]/best', 
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'nocheckcertificate': True,
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{song_name}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                return info['entries'][0]
            return None
    except Exception as e:
        print(f"yt-dlp error: {e}")
        return None

@api_view(['POST'])
def get_song_link(request):
    song_name = request.data.get('song_name')
    
    if not song_name:
        return Response({"error": "Song name is required"}, status=status.HTTP_400_BAD_REQUEST)

    # get_audio_info function ko call kiya
    video_data = get_audio_info(song_name)

    if video_data:
        return Response({
            "title": video_data.get('title'),
            "url": video_data.get('url'),
            "thumbnail": video_data.get('thumbnail'),
            "duration": video_data.get('duration')
        })
    else:
        return Response({"error": "Could not find song or YouTube blocked the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

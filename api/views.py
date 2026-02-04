import os
import yt_dlp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def get_audio_info(song_name):
    # Cookies file ka path (jahan manage.py hai)
    # views.py mein get_audio_info ke andar ye lines add karein:
    cookie_path = os.path.join(os.getcwd(), 'cookies.txt')
    print(f"Checking cookies at: {cookie_path}")
    print(f"File exists: {os.path.exists(cookie_path)}")

    ydl_opts = {
        'format': 'bestaudio/best',           # ← yeh safe hai
        # ya 'ba/bestaudio/best' 
        # ya 'bestaudio[ext=m4a]/bestaudio/best' agar m4a priority chahiye
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'nocheckcertificate': True,
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        'user_agent': '...',  # tera wala
        # Extra strong fallback (optional)
        'extractaudio': True,                 # agar format fail to audio extract
        'audioformat': 'm4a',
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

import os
import yt_dlp
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def get_audio_info(song_name):
    # 1. Cookies file ka rasta dhundo (ye manage.py ke sath honi chahiye)
    cookie_path = os.path.join(os.getcwd(), 'cookies.txt')
    
    # 2. Check karo file exist karti hai ya nahi (sirf debugging ke liye)
    if not os.path.exists(cookie_path):
        print("⚠️ Warning: cookies.txt file nahi mili! YouTube block kar sakta hai.")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'nocheckcertificate': True,
        # IMPORTANT: Ye line YouTube ko aapki identity dikhayegi
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Song search karo
            info = ydl.extract_info(f"ytsearch1:{song_name}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                video = info['entries'][0]
                return {
                    "title": video.get('title'),
                    "url": video.get('url'),
                    "thumbnail": video.get('thumbnail'),
                    "duration": video.get('duration'),
                    "source": "youtube"
                }
            return None
    except Exception as e:
        print(f"❌ yt-dlp Error: {str(e)}")
        return None

@api_view(['POST'])
def search_song(request):
    song_name = request.data.get('song_name')
    
    if not song_name:
        return Response({"error": "Bhai, song_name toh bhejo!"}, status=status.HTTP_400_BAD_REQUEST)
    
    data = get_audio_info(song_name)
    
    if data:
        return Response(data)
    else:
        return Response({"error": "YouTube ne block kar diya ya song nahi mila. Cookies check karo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

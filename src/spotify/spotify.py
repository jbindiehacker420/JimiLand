import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

def get_current_track():
    """Get the currently playing track from your Spotify account"""
    load_dotenv()
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri="http://localhost:8000/callback",
        scope='user-read-currently-playing',
        open_browser=True
    ))
    
    # Get current track
    current = sp.current_user_playing_track()
    
    if current is None or current.get('item') is None:
        return None
        
    track = current['item']
    return {
        'name': track['name'],
        'artist': track['artists'][0]['name'],
        'album': track['album']['name'],
        'album_art': track['album']['images'][0]['url'] if track['album']['images'] else None,
        'url': track['external_urls']['spotify']
    }

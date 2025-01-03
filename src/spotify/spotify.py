import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_current_track():
    """Get the currently playing track from Spotify"""
    try:
        # Check if Spotify credentials are available
        if not all([os.getenv('SPOTIFY_CLIENT_ID'), 
                   os.getenv('SPOTIFY_CLIENT_SECRET'),
                   os.getenv('SPOTIFY_REDIRECT_URI')]):
            return None

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope="user-read-currently-playing"
        ))
        
        current_track = sp.current_user_playing_track()
        if current_track is not None:
            return {
                'name': current_track['item']['name'],
                'artist': current_track['item']['artists'][0]['name'],
                'album': current_track['item']['album']['name'],
                'album_art': current_track['item']['album']['images'][0]['url'],
                'url': current_track['item']['external_urls']['spotify']
            }
        return None
    except Exception as e:
        print(f"Error getting Spotify track: {e}")
        return None

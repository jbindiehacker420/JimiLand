import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

def get_spotify_token():
    """
    Run this script once to get your Spotify token.
    It will save the token in .cache file which our main app will use.
    """
    load_dotenv()
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri="http://localhost:8000/callback",
        scope='user-read-currently-playing user-read-recently-played user-top-read',
        open_browser=True
    ))
    
    # Test the connection
    current_track = sp.current_user_playing_track()
    if current_track:
        print(f"Successfully authenticated! Currently playing: {current_track['item']['name']}")
    else:
        print("Successfully authenticated! No track currently playing.")

if __name__ == "__main__":
    get_spotify_token()

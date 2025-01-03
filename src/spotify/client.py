import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import json
from dotenv import load_dotenv

class SpotifyClient:
    def __init__(self):
        load_dotenv()
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri="http://localhost:8000/callback",
            scope='user-read-currently-playing user-read-recently-played user-top-read',
            open_browser=False  # Don't open browser each time
        ))

    def get_current_track(self):
        try:
            result = self.sp.current_user_playing_track()
            if not result:
                return None
            
            return {
                'name': result['item']['name'],
                'artist': result['item']['artists'][0]['name'],
                'album': result['item']['album']['name'],
                'album_art': result['item']['album']['images'][0]['url'],
                'progress_ms': result['progress_ms'],
                'duration_ms': result['item']['duration_ms'],
                'spotify_url': result['item']['external_urls']['spotify'],
                'is_playing': result['is_playing']
            }
        except Exception as e:
            print(f"Error getting current track: {e}")
            return None

    def get_recently_played(self, limit=5):
        try:
            results = self.sp.current_user_recently_played(limit=limit)
            tracks = []
            for item in results['items']:
                track = item['track']
                tracks.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'album_art': track['album']['images'][0]['url'],
                    'spotify_url': track['external_urls']['spotify'],
                    'played_at': item['played_at']
                })
            return tracks
        except Exception as e:
            print(f"Error getting recently played tracks: {e}")
            return []

    def get_top_tracks(self, limit=10, time_range='short_term'):
        try:
            results = self.sp.current_user_top_tracks(limit=limit, time_range=time_range)
            return [{
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'album_art': track['album']['images'][0]['url'],
                'spotify_url': track['external_urls']['spotify']
            } for track in results['items']]
        except Exception as e:
            print(f"Error getting top tracks: {e}")
            return []

    def get_listening_data(self):
        """Get all listening data for the template"""
        return {
            'current_track': self.get_current_track(),
            'recently_played': self.get_recently_played(),
            'top_tracks': self.get_top_tracks(),
            'last_updated': datetime.now().isoformat()
        }

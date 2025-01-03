from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import os
from urllib.parse import urlparse, parse_qs
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle the callback from Spotify"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Parse the authorization code from the callback
        query_components = parse_qs(urlparse(self.path).query)
        
        # Show success message
        html = """
        <html>
            <body style="background: #121212; color: #ffffff; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
                <div style="text-align: center; padding: 2rem; background: #282828; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <h1 style="color: #1DB954;">Successfully Connected to Spotify!</h1>
                    <p>You can close this window and return to the application.</p>
                </div>
            </body>
        </html>
        """
        self.wfile.write(html.encode())

def start_auth_server():
    """Start local server to handle Spotify callback"""
    server = HTTPServer(('localhost', 8000), CallbackHandler)
    server.handle_request()  # Handle one request then close

def initialize_spotify():
    """Initialize Spotify client with proper authentication"""
    auth_manager = SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
        scope='user-read-currently-playing user-read-recently-played user-top-read'
    )
    
    # Start local server to handle callback
    start_auth_server()
    
    return spotipy.Spotify(auth_manager=auth_manager)

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from credentials_manager import get_credentials
# Get credentials
client_id, client_secret = get_credentials()
# Constants
CLIENT_ID = client_id
CLIENT_SECRET = client_secret
REDIRECT_URI = 'http://localhost:8888/callback'

def spotify_authenticate(scope):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                scope=scope))
    return sp
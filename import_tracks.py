import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from spotify_authenticate import spotify_authenticate
SCOPE = 'user-read-recently-played user-top-read'
# Get credentials
sp = spotify_authenticate(SCOPE)
top_tracks = sp.current_user_top_tracks(limit=50, time_range='medium_term')

track_data = []
for item in top_tracks['items']:
    track = {
        'name': item['name'],
        'artist': item['artists'][0]['name'],
        'album': item['album']['name'],
        'popularity': item['popularity'],
        'duration_ms': item['duration_ms']
    }
    track_data.append(track)

df_tracks = pd.DataFrame(track_data)
df_tracks.head()
# Analyse des genres les plus écoutés
top_artists = sp.current_user_top_artists(limit=50, time_range='medium_term')
artist_data = []
for artist in top_artists['items']:
    artist_info = {
        'name': artist['name'],
        'genres': ", ".join(artist['genres']),
        'popularity': artist['popularity']
    }
    artist_data.append(artist_info)

df_artists = pd.DataFrame(artist_data)
df_artists.head()

# Récupérer les morceaux récemment joués
recent_tracks = sp.current_user_recently_played(limit=50)

# Extraire les informations et les mettre dans un DataFrame
recent_data = []
for item in recent_tracks['items']:
    track = item['track']
    played_at = item['played_at']
    played_at_dt = datetime.datetime.strptime(played_at, '%Y-%m-%dT%H:%M:%S.%fZ')
    recent_data.append({
        'name': track['name'],
        'artist': track['artists'][0]['name'],
        'played_at': played_at_dt
    })

df_recent = pd.DataFrame(recent_data)
df_recent.head()

# Configuration de base pour les visualisations
sns.set_theme(style="whitegrid")

# Exemple de visualisation : Popularité des morceaux
plt.figure(figsize=(14, 7))
sns.barplot(x='popularity', y='name', data=df_tracks.sort_values('popularity', ascending=False))
plt.title('Top 50 des morceaux par popularité')
plt.xlabel('Popularité')
plt.ylabel('Morceaux')
plt.show()

# Exemple de visualisation : Durée des morceaux
plt.figure(figsize=(14, 7))
sns.histplot(df_tracks['duration_ms'] / 1000, bins=30, kde=True)
plt.title('Distribution des durées des morceaux')
plt.xlabel('Durée (secondes)')
plt.ylabel('Fréquence')
plt.show()


# Distribution des genres
plt.figure(figsize=(14, 7))
genre_list = df_artists['genres'].str.split(', ', expand=True).stack()
sns.countplot(y=genre_list, order=genre_list.value_counts().index)
plt.title('Distribution des genres les plus écoutés')
plt.xlabel('Nombre de morceaux')
plt.ylabel('Genres')
plt.show()

# Visualisation des heures d'écoute
df_recent['hour'] = df_recent['played_at'].dt.hour
plt.figure(figsize=(14, 7))
sns.histplot(df_recent['hour'], bins=24, kde=True)
plt.title('Distribution des heures d\'écoute')
plt.xlabel('Heure de la journée')
plt.ylabel('Nombre de morceaux écoutés')
plt.show()
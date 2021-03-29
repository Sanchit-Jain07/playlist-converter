import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import re
import pprint
# from youtube import get_playlist_songs



# titles, name = get_playlist_songs('OLAK5uy_l0EQmItW0hIlXpMG-ZB7N3t5CHFmkjnbQ')
# scope = 'playlist-modify-public'
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def create_spotify_playlist(sp, titles, name):
    words = ['official', 'audio', 'video', 'lyrics', 'music', 'ft', 'feat', 'vevo']
    songs=[]

    unable=[]
    for title in titles:
        search = title.lower()
        resultwords = [word for word in re.split("\W+",search) if word.lower() not in words]
        resultwords = ' '.join(resultwords)
        resultwords = re.sub(r'/\(.*?\)|\[.*?\]/g', "", resultwords)

        result = sp.search(resultwords, type='track', limit=1)

        if not result['tracks']['items']:
            unable.append(title)
            continue
        songs.append({'name': result['tracks']['items'][0]['name'], 'uri': result['tracks']['items'][0]['uri']})

    uid =  sp.current_user()['id']
    playlist = sp.user_playlist_create(uid, name,)
    playlist_id = playlist['id']
    n=0
    while songs[n:n+100]:
        tracks_add = sp.user_playlist_add_tracks(uid, playlist_id, [song['uri'] for song in songs[n:n+100]])
        n+=100

    print("OK!")
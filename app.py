from flask import Flask, redirect, render_template, url_for, request, session, flash, jsonify
import spotipy
import os
import time
import json
from youtube import get_playlist_songs
from spotify import create_spotify_playlist
# from utils import get_all_top_tracks, get_all_top_artists, get_audio_features, get_recommended_artists, get_recommendations, get_user, create_playlist
os.environ['SPOTIPY_CLIENT_ID'] = '58678ff94eae4339a525074449dc013e'
os.environ['SPOTIPY_CLIENT_SECRET'] = '9315af7bbec44e93b8cdb1082ffe14e4'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1/5000'
app = Flask(__name__)
app.secret_key = 'secretverysecret'

SCOPE = 'playlist-modify-public'

@app.before_request
def before_request():
    if os.path.exists(".cache"):
        os.remove(".cache")

@app.route('/verify')
def verify():
    sp_auth = spotipy.oauth2.SpotifyOAuth(scope=SCOPE)
    auth_url = sp_auth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_auth = spotipy.oauth2.SpotifyOAuth(scope=SCOPE)
    session.clear()
    code = request.args.get('code')
    
    token_info = sp_auth.get_access_token(code=code)
    session['token_info'] = token_info

    return redirect(url_for('info'))

@app.route('/info/<id>')
def info(id):
    session['token_info'], authorized = get_token(session)
    session.modified = True
    if not authorized:
        flash("Please Login with your Spotify Account")
        return redirect('/')

    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))

    titles, name = get_playlist_songs(id)
    create_spotify_playlist(sp, titles, name)

    return jsonify('EPIC')


@app.route('/logout')
def logout():
    session['token_info'], authorized = get_token(session)
    session.modified = True
    if not authorized:
        flash('You are already Logged out!')
        return redirect('/')
    
    session.pop('token_info')
    flash('You have successfully Logged Out!')
    return redirect('/')

# Checks to see if token is valid and gets a new token if not
def get_token(session):
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
        sp_oauth = spotipy.oauth2.SpotifyOAuth(scope = SCOPE)
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

if __name__ == "__main__":
    app.run(debug=True)
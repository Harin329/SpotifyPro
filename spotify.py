from flask import Flask, jsonify, request, make_response, redirect
from dotenv import load_dotenv
from functions import getToken, getUserInformation, skipSong, getTrackInfo
import time
import os

load_dotenv()

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
redirect_uri = os.environ['REDIRECT_URI']
scopes = os.environ['SCOPES']

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']
session = {}

@app.route("/")
def welcome():
    return 'Welcome to SpotifyPro, Harin & Anna!'

@app.route("/healthcheck")
def healthcheck():
    return jsonify(status='successful')

@app.route('/authorize')
def authorize():
    authorize_url = 'https://accounts.spotify.com/en/authorize?'
    parameters = 'response_type=code&client_id=' + client_id + '&redirect_uri=' + redirect_uri + '&scope=' + scopes
    response = make_response(redirect(authorize_url + parameters))
    return response

@app.route('/callback')
def callback():
    global session
    if request.args.get('error'):
	    return "Spotify error"
    else:
        code = request.args.get('code')
        payload = getToken(code)
        if payload != None:
            session['token'] = payload[0]
            session['refresh_token'] = payload[1]
            session['token_expiration'] = time.time() + payload[2]
        else:
            return "Failed to access token"

    current_user = getUserInformation(session)
    session['user_id'] = current_user['id']

    return "Auth Success"

@app.route("/api/moveSong", methods = ['GET'])
def moveSong():
    global session
    year = getTrackInfo(session)
    print(year)
    # Put Song in Year Album
    # Remove Song From Current
    skipSong(session)

    return "Song Moved!"
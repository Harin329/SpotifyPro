import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

authorization = os.environ['AUTHORIZATION']
redirect_uri = os.environ['REDIRECT_URI']

def getToken(code):
	token_url = 'https://accounts.spotify.com/api/token'
	headers = {'Authorization': authorization, 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
	body = {'code': code, 'redirect_uri': redirect_uri, 'grant_type': 'authorization_code'}
	post_response = requests.post(token_url, headers=headers, data=body)

	if post_response.status_code == 200:
		json = post_response.json()
		return json['access_token'], json['refresh_token'], json['expires_in']
	else:
		return None

def refreshToken(refresh_token):
	token_url = 'https://accounts.spotify.com/api/token'
	headers = {'Authorization': authorization, 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
	body = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
	post_response = requests.post(token_url, headers=headers, data=body)

	if post_response.status_code == 200:
		return post_response.json()['access_token'], post_response.json()['expires_in']
	else:
		return None

def checkTokenStatus(session):
	if time.time() > session['token_expiration']:
		payload = refreshToken(session['refresh_token'])

		if payload != None:
			session['token'] = payload[0]
			session['token_expiration'] = time.time() + payload[1]
		else:
			return None

	return "Success"

def makeGetRequest(session, url, params={}):
	headers = {"Authorization": "Bearer {}".format(session['token'])}
	response = requests.get(url, headers=headers, params=params)

	if response.status_code == 200:
		return response.json()

	elif response.status_code == 401 and checkTokenStatus(session) != None:
		return makeGetRequest(session, url, params)
	else:
		return None

def makePutRequest(session, url, params={}, data={}):
	headers = {"Authorization": "Bearer {}".format(session['token']), 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
	response = requests.put(url, headers=headers, params=params, data=data)

	if response.status_code == 204 or response.status_code == 403 or response.status_code == 404 or response.status_code == 500:
		return response.status_code

	elif response.status_code == 401 and checkTokenStatus(session) != None:
		return makePutRequest(session, url, data)
	else:
		return None

def makePostRequest(session, url, data):
	headers = {"Authorization": "Bearer {}".format(session['token']), 'Accept': 'application/json', 'Content-Type': 'application/json'}
	response = requests.post(url, headers=headers, data=data)

	if response.status_code == 201:
		return response.json()
	if response.status_code == 204:
		return response

	elif response.status_code == 401 and checkTokenStatus(session) != None:
		return makePostRequest(session, url, data)
	elif response.status_code == 403 or response.status_code == 404:
		return response.status_code
	else:
		return None

def makeDeleteRequest(session, url, data):
	headers = {"Authorization": "Bearer {}".format(session['token']), 'Accept': 'application/json', 'Content-Type': 'application/json'}
	response = requests.delete(url, headers=headers, data=data)

	if response.status_code == 200:
		return response.json()

	elif response.status_code == 401 and checkTokenStatus(session) != None:
		return makeDeleteRequest(session, url, data)
	else:
		return None

def getUserInformation(session):
	url = 'https://api.spotify.com/v1/me'
	payload = makeGetRequest(session, url)

	if payload == None:
		return None

	return payload

def skipSong(session):
	url = 'https://api.spotify.com/v1/me/player/next'
	data = {}
	payload = makePostRequest(session, url, data)

	if payload == None:
		return None

	return payload

def getTrackInfo(session):
	url = 'https://api.spotify.com/v1/me/player/currently-playing'
	payload = makeGetRequest(session, url)

	if payload == None :
		return None

	name = payload['item']['name']
	trackID = payload['item']['id']
	year = getYear(session, trackID)
	uri = payload['item']['uri']

	print(name)

	return {'year': year, 'uri': uri}

def getYear(session, trackID):
	url = 'https://api.spotify.com/v1/tracks/' + trackID
	payload = makeGetRequest(session, url)

	if payload == None :
		return None

	return payload['album']['release_date'][0:4]

def getYearPlaylist(session, year, limit=20):
	url = 'https://api.spotify.com/v1/me/playlists'
	offset = 0
	playlist = None

	total = 1
	while total > offset:
		params = {'limit': limit, 'offset': offset}
		payload = makeGetRequest(session, url, params)

		if payload == None:
			return None
		
		for item in payload['items']:
			if item['name'] == str(year):
				playlist = item

		total = payload['total']
		offset += limit

	print(playlist)

	return playlist

def getCurrentPlaylist(session, limit=20):
	url = 'https://api.spotify.com/v1/me/playlists'
	offset = 0
	playlist = None

	total = 1
	while total > offset:
		params = {'limit': limit, 'offset': offset}
		payload = makeGetRequest(session, url, params)

		if payload == None:
			return None
		
		for item in payload['items']:
			if item['name'] == 'Current':
				playlist = item

		total = payload['total']
		offset += limit

	return playlist

def addToPlaylist(session, year, uri):
	playlist_id = getYearPlaylist(session, year)
	playlist_id = playlist_id['id']
	url = 'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks'

	uri_str = ""
	uri_str += "\"" + uri + "\","

	data = "{\"uris\": [" + uri_str[0:-1] + "]}"
	makePostRequest(session, url, data)

	return "Success"

def removeFromCurrent(session, uri):
	playlist_id = getCurrentPlaylist(session)
	playlist_id = playlist_id['id']
	url = 'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks'

	uri_str = ""
	uri_str += "\"" + uri + "\","

	data = "{\"uris\": [" + uri_str[0:-1] + "]}"
	makeDeleteRequest(session, url, data)

	return "Success"
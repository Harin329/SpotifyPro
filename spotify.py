from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
    return 'Welcome to SpotifyPro, Harin & Anna!'

@app.route("/api/healthcheck")
def healthcheck():
    return jsonify(status='success')

@app.route("/api/moveSong")
def welcome():
    return 'This song will be properly classified!'
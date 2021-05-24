from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
    return 'Welcome to Spotify, Harin & Anna!'

@app.route("/api/healthcheck")
def healthcheck():
    return jsonify(status='success')
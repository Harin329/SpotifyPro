from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
    return 'Welcome, Harin Wu!'

@app.route("/api/healthcheck")
def healthcheck():
    return jsonify(status='success')
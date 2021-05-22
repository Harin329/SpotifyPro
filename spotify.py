from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
    return 'Welcome, Hao!'

@app.route("/api/healthcheck")
def healthcheck():
    return jsonify(status='success')
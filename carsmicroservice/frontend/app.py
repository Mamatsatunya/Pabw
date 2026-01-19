from flask import Flask
import requests

app = Flask(__name__)

@app.route("/ms1")
def ms1():
    return requests.get("http://localhost:5051/cars").json()

@app.route("/ms2")
def ms2():
    return requests.get("http://localhost:5052/cars/merge").json()

@app.route("/ms3")
def ms3():
    return requests.get("http://localhost:5053/cars").json()

app.run(port=5000)

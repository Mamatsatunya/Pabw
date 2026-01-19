from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = "../database/carsweb.db"

def connect():
    return sqlite3.connect(DB)

@app.route("/cars", methods=["GET"])
def get_cars():
    con = connect()
    cur = con.cursor()
    cars = cur.execute("SELECT * FROM cars").fetchall()
    con.close()
    return jsonify(cars)

@app.route("/cars", methods=["POST"])
def add_car():
    data = request.json
    con = connect()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO cars (brand, model, year, price) VALUES (?,?,?,?)",
        (data["brand"], data["model"], data["year"], data["price"])
    )
    con.commit()
    con.close()
    return {"status": "success"}
    
app.run(port=5051)

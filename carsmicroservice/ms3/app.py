from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DB = "../database/carsweb.db"

@app.route("/cars")
def cars():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    data = cur.execute("SELECT * FROM cars").fetchall()
    con.close()
    return jsonify(data)

app.run(port=5053)

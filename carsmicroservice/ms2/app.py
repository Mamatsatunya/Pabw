from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DBA = "../database/carsweb.db"
DBB = "../database/carsweb.db"

def read(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    data = cur.execute("SELECT * FROM cars").fetchall()
    con.close()
    return data

@app.route("/cars/merge")
def merge():
    return jsonify({
        "DB-A": read(DBA),
        "DB-B": read(DBB)
    })

app.run(port=5052)

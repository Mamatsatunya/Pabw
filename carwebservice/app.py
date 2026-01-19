from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "carsweb.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ========================
# READ ALL CARS
# ========================
@app.route('/cars', methods=['GET'])
def get_cars():
    conn = get_db()
    cars = conn.execute("SELECT * FROM cars").fetchall()
    conn.close()
    return jsonify([dict(car) for car in cars])

# ========================
# READ CAR BY ID
# ========================
@app.route('/cars/<int:id>', methods=['GET'])
def get_car(id):
    conn = get_db()
    car = conn.execute("SELECT * FROM cars WHERE id=?", (id,)).fetchone()
    conn.close()
    if car:
        return jsonify(dict(car))
    return jsonify({"message": "Car not found"}), 404

# ========================
# CREATE CAR
# ========================
@app.route('/cars', methods=['POST'])
def add_car():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO cars (brand, model, year, price) VALUES (?, ?, ?, ?)",
        (data['brand'], data['model'], data['year'], data['price'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Car added"}), 201

# ========================
# UPDATE CAR
# ========================
@app.route('/cars/<int:id>', methods=['PUT'])
def update_car(id):
    data = request.json
    conn = get_db()
    conn.execute(
        "UPDATE cars SET brand=?, model=?, year=?, price=? WHERE id=?",
        (data['brand'], data['model'], data['year'], data['price'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Car updated"})

# ========================
# DELETE CAR
# ========================
@app.route('/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    conn = get_db()
    conn.execute("DELETE FROM cars WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Car deleted"})

if __name__ == '__main__':
    app.run(debug=True)

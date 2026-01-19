from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = 'carsweb.db'

def get_db():
    return sqlite3.connect(DB_NAME)

@app.route('/')
def index():
    db = get_db()
    cars = db.execute("SELECT * FROM cars").fetchall()
    db.close()
    return render_template('index.html', cars=cars)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']

        db = get_db()
        db.execute(
            "INSERT INTO cars (brand, model, year, price) VALUES (?, ?, ?, ?)",
            (brand, model, year, price)
        )
        db.commit()
        db.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    db = get_db()
    car = db.execute("SELECT * FROM cars WHERE id=?", (id,)).fetchone()

    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']

        db.execute(
            "UPDATE cars SET brand=?, model=?, year=?, price=? WHERE id=?",
            (brand, model, year, price, id)
        )
        db.commit()
        db.close()
        return redirect(url_for('index'))

    db.close()
    return render_template('edit.html', car=car)

@app.route('/delete/<int:id>')
def delete(id):
    db = get_db()
    db.execute("DELETE FROM cars WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

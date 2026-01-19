from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret123'

def get_db():
    return sqlite3.connect("database.db")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        e = request.form['email']
        db = get_db()
        db.execute("INSERT INTO users VALUES (NULL,?,?,?)",(u,p,e))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p)).fetchone()
        if user:
            session['user'] = u
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        text = request.form['text']
        time = datetime.now()
        db = get_db()
        db.execute("INSERT INTO posts VALUES (NULL,?,?,?)",(session['user'],text,time))
        db.commit()

    return render_template('dashboard.html', user=session['user'])

@app.route('/profile/<username>')
def profile(username):
    db = get_db()
    posts = db.execute("SELECT text,time FROM posts WHERE username=?",(username,)).fetchall()
    return render_template('profile.html', posts=posts, username=username)

@app.route('/admin')
def admin():
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    posts = db.execute("SELECT * FROM posts").fetchall()
    return render_template('admin.html', users=users, posts=posts)

app.run(debug=True)

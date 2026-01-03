from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secretkey123"
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect("users.db")

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- ROUTES ----------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            return redirect('/dashboard')
        else:
            return "Invalid login"
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template("register.html")

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?,?)",
                    (username, password))
        conn.commit()
        conn.close()
        return redirect('/')
    except:
        return "User already exists"

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                (username, password))
    user = cur.fetchone()
    conn.close()

    if user:
        session['user'] = username
        return redirect('/home')
    else:
        return "Invalid Login"

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template("index.html")

@app.route('/design', methods=['POST'])
def design():
    if 'user' not in session:
        return redirect('/')

    area = int(request.form['area'])
    image = request.files.get('image')

    if area < 600:
        layout = "1BHK Compact Design"
    elif area < 1200:
        layout = "2BHK Modern Design"
    else:
        layout = "3BHK Luxury Design"

    colors = ["White & Grey", "Beige & Brown", "Blue & White"]

    if image:
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        ai_note = "AI analyzed image and suggested modern design."
    else:
        ai_note = "Design based on area."

    return render_template("index.html",
                           layout=layout,
                           colors=colors,
                           ai_note=ai_note)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

import os
from flask import send_from_directory

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/generate', methods=['POST'])
def generate():
    area = request.form['area']
    image = request.files.get('image')
    image_url = None

    # Save uploaded image
    if image and image.filename != '':
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)
        image_url = f'/static/uploads/{image.filename}'

    # Placeholder AI logic
    design = f"Suggested layout for {area} sq ft: Open plan with modern furniture placement."

    # Color suggestions
    colors = ["#FF5733", "#33FFCE", "#335BFF"]

    return render_template('dashboard.html', design=design, colors=colors, image_url=image_url)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)


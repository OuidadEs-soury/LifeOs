from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import random
import datetime

app = Flask(__name__)
app.secret_key = "lifeos_secret"


def db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    d = db()

    d.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    d.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        status TEXT,
        date TEXT
    )
    """)

    d.execute("""
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT
    )
    """)

    user = d.execute("SELECT * FROM users WHERE username='admin'").fetchone()

    if not user:
        d.execute(
            "INSERT INTO users (username,password) VALUES (?,?)",
            ("admin","lifeos123")
        )

    d.commit()


@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")


@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = db().execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        ).fetchone()

        if user:
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/dashboard")
def dashboard():

    tasks = db().execute("SELECT * FROM tasks").fetchall()

    total = len(tasks)
    done = len([t for t in tasks if t["status"] == "done"])

    productivity = 0
    if total > 0:
        productivity = int((done/total)*100)

    return render_template(
        "dashboard.html",
        tasks=tasks,
        productivity=productivity
    )


@app.route("/tasks")
def tasks():

    tasks = db().execute("SELECT * FROM tasks").fetchall()

    return render_template("tasks.html",tasks=tasks)


@app.route("/add_task", methods=["POST"])
def add_task():

    title = request.form["title"]

    today = str(datetime.date.today())

    d = db()

    d.execute(
        "INSERT INTO tasks (title,status,date) VALUES (?,?,?)",
        (title,"todo",today)
    )

    d.commit()

    return redirect("/tasks")


@app.route("/update_task", methods=["POST"])
def update_task():

    data = request.get_json()

    d = db()

    d.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        (data["status"],data["task_id"])
    )

    d.commit()

    return jsonify({"success":True})


@app.route("/calendar")
def calendar():

    tasks = db().execute("SELECT * FROM tasks").fetchall()

    return render_template("calendar.html",tasks=tasks)


if __name__ == "__main__":

    init_db()

    app.run(debug=True)
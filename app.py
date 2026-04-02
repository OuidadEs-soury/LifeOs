from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import random

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
        status TEXT
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

    notes = db().execute("SELECT * FROM notes").fetchall()

    productivity = random.randint(60,100)

    return render_template(
        "dashboard.html",
        tasks=tasks,
        notes=notes,
        productivity=productivity
    )


@app.route("/tasks")
def tasks():

    tasks = db().execute("SELECT * FROM tasks").fetchall()

    return render_template("tasks.html",tasks=tasks)


@app.route("/add_task", methods=["POST"])
def add_task():

    title = request.form["title"]

    d = db()

    d.execute(
        "INSERT INTO tasks (title,status) VALUES (?,?)",
        (title,"todo")
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


@app.route("/notes")
def notes():

    notes = db().execute("SELECT * FROM notes").fetchall()

    return render_template("notes.html",notes=notes)


@app.route("/add_note", methods=["POST"])
def add_note():

    content = request.form["content"]

    d = db()

    d.execute(
        "INSERT INTO notes (content) VALUES (?)",
        (content,)
    )

    d.commit()

    return redirect("/notes")


# AI assistant

@app.route("/ai")
def ai():

    return render_template("ai.html")


@app.route("/ask_ai", methods=["POST"])
def ask_ai():

    q = request.get_json()["question"]

    responses = [
        "Focus on one task at a time.",
        "Break the task into smaller steps.",
        "Take a 5 minute break and come back.",
        "Your productivity is great today.",
        "Remember why you started."
    ]

    return jsonify({
        "answer": random.choice(responses)
    })


if __name__ == "__main__":

    init_db()

    app.run(debug=True)
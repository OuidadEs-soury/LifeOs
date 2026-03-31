from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "lifeos_secret"


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    db = get_db()

    db.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        status TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT
    )
    """)

    user = db.execute("SELECT * FROM users WHERE username='admin'").fetchone()

    if not user:
        db.execute(
            "INSERT INTO users (username,password) VALUES (?,?)",
            ("admin","lifeos123")
        )

    db.commit()


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

        db = get_db()

        user = db.execute(
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

    if "user" not in session:
        return redirect("/login")

    db = get_db()

    tasks = db.execute("SELECT * FROM tasks").fetchall()

    notes = db.execute("SELECT * FROM notes").fetchall()

    return render_template("dashboard.html", tasks=tasks, notes=notes)


@app.route("/tasks")
def tasks():

    db = get_db()

    tasks = db.execute("SELECT * FROM tasks").fetchall()

    return render_template("tasks.html", tasks=tasks)


@app.route("/add_task", methods=["POST"])
def add_task():

    title = request.form["title"]

    db = get_db()

    db.execute(
        "INSERT INTO tasks (title,status) VALUES (?,?)",
        (title,"todo")
    )

    db.commit()

    return redirect("/tasks")


@app.route("/update_task", methods=["POST"])
def update_task():

    data = request.get_json()

    db = get_db()

    db.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        (data["status"],data["task_id"])
    )

    db.commit()

    return jsonify({"success":True})


@app.route("/notes")
def notes():

    db = get_db()

    notes = db.execute("SELECT * FROM notes").fetchall()

    return render_template("notes.html",notes=notes)


@app.route("/add_note", methods=["POST"])
def add_note():

    content = request.form["content"]

    db = get_db()

    db.execute(
        "INSERT INTO notes (content) VALUES (?)",
        (content,)
    )

    db.commit()

    return redirect("/notes")


if __name__ == "__main__":

    init_db()

    app.run(debug=True)
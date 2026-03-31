from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    db = get_db()

    db.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'todo'
    )
    """)

    db.commit()


@app.route("/")
def home():
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():

    db = get_db()

    tasks = db.execute("SELECT * FROM tasks").fetchall()

    return render_template("dashboard.html", tasks=tasks)


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
        "INSERT INTO tasks (title, status) VALUES (?, 'todo')",
        (title,)
    )

    db.commit()

    return redirect("/tasks")


@app.route("/update_task", methods=["POST"])
def update_task():

    data = request.get_json()

    task_id = data["task_id"]
    status = data["status"]

    db = get_db()

    db.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        (status, task_id)
    )

    db.commit()

    return jsonify({"success": True})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
from flask import Blueprint, render_template, request, redirect, session
from database.db import get_db

tasks = Blueprint("tasks", __name__)


@tasks.route("/dashboard")
def dashboard():

    db = get_db()

    tasks = db.execute(
        "SELECT * FROM tasks WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    return render_template("dashboard.html", tasks=tasks)


@tasks.route("/add_task", methods=["POST"])
def add_task():

    title = request.form["title"]

    db = get_db()

    db.execute(
        "INSERT INTO tasks(user_id,title,status) VALUES (?,?,?)",
        (session["user_id"], title, "todo")
    )

    db.commit()

    return redirect("/dashboard")
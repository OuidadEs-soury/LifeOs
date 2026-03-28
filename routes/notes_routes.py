from flask import Blueprint, render_template, request, redirect, session
from database.db import get_db

notes = Blueprint("notes", __name__)


@notes.route("/notes")
def notes_page():

    db = get_db()

    notes = db.execute(
        "SELECT * FROM notes WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    return render_template("notes.html", notes=notes)


@notes.route("/add_note", methods=["POST"])
def add_note():

    content = request.form["content"]

    db = get_db()

    db.execute(
        "INSERT INTO notes(user_id,content) VALUES (?,?)",
        (session["user_id"], content)
    )

    db.commit()

    return redirect("/notes")
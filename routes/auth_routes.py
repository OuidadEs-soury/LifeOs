from flask import Blueprint, render_template, request, redirect, session
from database.db import get_db

auth = Blueprint("auth", __name__)


@auth.route("/")
def home():
    return redirect("/login")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = get_db()

        user = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        if user:
            session["user_id"] = user["id"]
            return redirect("/dashboard")

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = get_db()

        db.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (username, password)
        )

        db.commit()

        return redirect("/login")

    return render_template("register.html")
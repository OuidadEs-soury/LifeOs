from flask import Flask, render_template, request, redirect, session
from database import get_db, init_db

app = Flask(__name__)
app.secret_key = "secret"

init_db()


@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
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
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    db = get_db()

    tasks = db.execute("SELECT * FROM tasks").fetchall()

    return render_template("dashboard.html", tasks=tasks)


@app.route("/add_task", methods=["POST"])
def add_task():

    title = request.form["title"]

    db = get_db()

    db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    db.commit()

    return redirect("/dashboard")


@app.route("/complete/<int:id>")
def complete(id):

    db = get_db()

    db.execute("UPDATE tasks SET completed=1 WHERE id=?", (id,))
    db.commit()

    return redirect("/dashboard")


app.run(debug=True)
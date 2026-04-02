from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.secret_key = "lifeos_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)


@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "lifeos123":
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    tasks = Task.query.all()

    total = len(tasks)
    completed = len([t for t in tasks if t.completed])

    productivity = 0
    if total > 0:
        productivity = int((completed / total) * 100)

    return render_template(
        "dashboard.html",
        tasks=tasks,
        productivity=productivity
    )


@app.route("/tasks", methods=["GET","POST"])
def tasks():

    if request.method == "POST":
        title = request.form["title"]
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.all()

    return render_template("tasks.html", tasks=tasks)


@app.route("/complete/<int:id>")
def complete(id):

    task = Task.query.get(id)
    task.completed = True
    db.session.commit()

    return redirect("/tasks")


@app.route("/ai", methods=["GET","POST"])
def ai():

    answer = ""

    if request.method == "POST":

        prompt = request.form["prompt"]

        try:

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": "Bearer YOUR_OPENAI_KEY",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages":[
                        {"role":"user","content":prompt}
                    ]
                }
            )

            data = response.json()

            answer = data["choices"][0]["message"]["content"]

        except:
            answer = "AI service unavailable."

    return render_template("ai.html", answer=answer)


if __name__ == "__main__":
    app.run(debug=True)
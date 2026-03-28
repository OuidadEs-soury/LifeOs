from flask import Flask
from database.db import init_db

app = Flask(__name__)
app.secret_key = "lifeos_secret"

init_db()

from routes.auth_routes import auth
from routes.task_routes import tasks
from routes.notes_routes import notes

app.register_blueprint(auth)
app.register_blueprint(tasks)
app.register_blueprint(notes)

if __name__ == "__main__":
    app.run(debug=True)
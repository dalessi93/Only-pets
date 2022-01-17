from flask import Flask, render_template, session
import os
import psycopg2
from werkzeug.utils import redirect
from controllers.session_controller import session_controller
from controllers.actions_controller import actions_controller


DB_URL = os.environ.get("DATABASE_URL", "dbname=project2")
SECRET_KEY = os.environ.get("SECRET_KEY", "password")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    if session.get("user_id"):
        return redirect("/home")
    else:
        return redirect("/login")

# @app.route('/')
# def index():
#   conn = psycopg2.connect(DB_URL)
#   cur = conn.cursor()
#   cur.execute('SELECT 1', []) # Query to check that the DB connected
#   conn.close()
#   return 'Hello, world!'

app.register_blueprint(session_controller)
app.register_blueprint(actions_controller)

if __name__ == "__main__":
    app.run(debug=True)
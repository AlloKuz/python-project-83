from page_analyzer.db import get_conn

from flask import Flask
from flask import render_template


app = Flask(__name__)
conn = create_connection()


@app.route("/")
def index():
    return render_template("index.html")

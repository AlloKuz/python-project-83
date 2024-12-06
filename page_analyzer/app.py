from page_analyzer.db import create_connection

from flask import Flask
from flask import render_template, request

from datetime import datetime


app = Flask(__name__)
conn = create_connection()


def is_valid(url):
    return True


def save_data(conn, url):
    with conn.cursor() as curs:
        curs.execute("""INSERT INTO urls (name, created_at) VALUES
                        (%s, %s)""", [url, datetime.now()])
    conn.commit()


def select_all(conn):
    with conn.cursor() as curs:
        curs.execute("""SELECT name, created_at FROM urls""")
        data = curs.fetchall()
    return data


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=['POST', 'GET'])
def urls():
    if request.method == "POST":
        # save the data
        url = request.form.get("url")
        save_data(conn, url)
    # show all the data
    all_urls = select_all(conn)
    return render_template("all_urls_page.html",
                           urls=all_urls if all_urls else [])

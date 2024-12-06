from page_analyzer.db import save_data, select_all, find_url_by_id
from page_analyzer.utils import url_validator, url_normalize

from flask import Flask
from flask import render_template, request, flash, redirect, url_for
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=["GET"])
def urls_get():
    all_urls = select_all() or []
    return render_template("all_urls_page.html",
                           urls=all_urls)


@app.route("/urls", methods=["POST"])
def urls_post():
    data = request.form.to_dict()
    errors = url_validator(data)
    if errors:
        return render_template("index.html", data=data, errors=errors), 422
    new_url = url_normalize(data["url"])
    save_data(new_url)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("urls_get"))


@app.route("/urls/<id_>", methods=["GET"])
def url_show(id_):
    data = find_url_by_id(id_)
    return render_template("show.html",
                           data=data)

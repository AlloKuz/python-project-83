from page_analyzer.db import (save_data,
                              get_checks_by_url_id, get_lastcheck_info,
                              find_url_by_id, find_url_by_name,
                              save_check)
from page_analyzer.utils import url_validate, url_normalize
from page_analyzer.parser import parse_html

from flask import Flask
from flask import render_template, request, flash, redirect, url_for
import os
import requests
import uuid
import logging


DEBUG = os.getenv("FLASK_DEBUG")

logger = logging.getLogger(__name__)


def use_dotenv():
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except Exception as e:
        logger.info(e)


def create_app():

    use_dotenv()

    logging.basicConfig(level=(logging.INFO if not DEBUG else logging.DEBUG))
    if DEBUG:
        logger.info("FLASK_DEBUG is on!")

    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") or uuid.uuid4()
    app.config['DATABASE_URL'] = os.getenv("DATABASE_URL")

    return app


app = create_app()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=["GET"])
def urls_get():
    all_urls = get_lastcheck_info()
    return render_template("all_urls_page.html",
                           urls=all_urls)


@app.route("/urls/<int:id_>", methods=["GET"])
def urls_show(id_):
    data = find_url_by_id(id_)
    checks = get_checks_by_url_id(id_)
    return render_template("show.html",
                           data=data,
                           checks=checks)


@app.route("/urls", methods=["POST"])
def urls_post():
    data = request.form.to_dict()
    errors = url_validate(data)
    if errors:
        flash("Некорректный URL", "danger")
        return render_template("index.html", data=data, errors=errors), 422

    try:
        new_url = url_normalize(data["url"])
        old_data = find_url_by_name(new_url)
        if old_data:
            flash("Страница уже существует", "info")
            return redirect(url_for("urls_show", id_=old_data["id"]))

        save_data(new_url)
        flash("Страница успешно добавлена", "success")
        new_data = find_url_by_name(new_url)
        return redirect(url_for("urls_show", id_=new_data["id"]))
    except Exception as e:
        flash("Произошла ошибка при проверке", "danger")
        logger.error(e)
    return redirect(url_for("urls_get"))


@app.route("/urls/<int:id_>/check", methods=["POST"])
def urls_check(id_):
    try:
        url_data = find_url_by_id(id_)
        status_code = None

        req = requests.get(url_data["name"])
        status_code = req.status_code
        req.raise_for_status()

        parsed_data = parse_html(requests.get(url_data["name"]).text)

        if not parsed_data:
            raise Exception("Ошибка при проверке!")
        save_check(id_,
                   status_code=status_code,
                   title=parsed_data["title"],
                   h1=parsed_data["h1"],
                   description=parsed_data["description"])
        flash("Страница успешно проверена", "success")
    except Exception as e:
        flash("Произошла ошибка при проверке", "danger")
        logger.error(e)
    return redirect(url_for("urls_show", id_=id_))

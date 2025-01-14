import logging
import os
import uuid

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer.db import (
    find_url_by_id,
    find_url_by_name,
    get_checks_by_url_id,
    get_urls_with_last_checks,
    save_check,
    save_url,
)
from page_analyzer.parser import parse_html
from page_analyzer.utils import url_normalize, url_validate

load_dotenv()

logger = logging.getLogger(__name__)

DEBUG = os.getenv("FLASK_DEBUG")


def create_app():

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
    get_urls_with_lastcheck_info = get_urls_with_last_checks()
    return render_template("all_urls_page.html",
                           urls=get_urls_with_lastcheck_info)


@app.route("/urls/<int:id_>", methods=["GET"])
def urls_show(id_):
    data = find_url_by_id(id_)
    if not data:
        return "Page not found", 404
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

        new_data = save_url(new_url)
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("urls_show", id_=new_data["id"]))
    except Exception as e:
        flash("Произошла ошибка при проверке", "danger")
        logger.error(e)
    return redirect(url_for("urls_get"))


@app.route("/urls/<int:id_>/check", methods=["POST"])
def urls_check(id_):
    url_data = find_url_by_id(id_)

    try:
        response = requests.get(url_data["name"])
        response.raise_for_status()

        parsed_data = parse_html(response.text)

        save_check(
            id_,
            status_code=response.status_code,
            title=parsed_data["title"],
            h1=parsed_data["h1"],
            description=parsed_data["description"]
        )
        flash("Страница успешно проверена", "success")
    except requests.RequestException as e:
        flash("Произошла ошибка при проверке URL", "danger")
        logger.error(e)
    except Exception as e:
        flash("Произошла ошибка при обработке данных", "danger")
        logger.error(e)

    return redirect(url_for("urls_show", id_=id_))

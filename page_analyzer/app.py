from page_analyzer.db import save_data, select_all
from page_analyzer.utils import is_url_valid

from flask import Flask
from flask import render_template, request, flash
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=['POST', 'GET'])
def urls():
    if request.method == "POST":
        # save the data
        url = request.form.get("url")
        if is_url_valid(url):
            save_data(url)
        else:
            # flash error
            flash("Wrong URL! Try again")
            return render_template("index.html",
                                   value=url)
    # show all the data
    all_urls = select_all()
    return render_template("all_urls_page.html",
                           urls=all_urls if all_urls else [])

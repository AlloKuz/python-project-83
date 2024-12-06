from page_analyzer.db import save_data, select_all


from flask import Flask
from flask import render_template, request


app = Flask(__name__)


def is_valid(url):
    return True


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=['POST', 'GET'])
def urls():
    if request.method == "POST":
        # save the data
        url = request.form.get("url")
        save_data(url)
    # show all the data
    all_urls = select_all()
    return render_template("all_urls_page.html",
                           urls=all_urls if all_urls else [])

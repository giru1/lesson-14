from flask import render_template, request
from db.index import titles
from app import app


@app.route('/', methods=["GET", "POST"])
def index():
    """
    Обработка главной страницы
    """
    # for title in titles:
    #     print(type(title))
    return render_template('index.html', titles=titles)


@app.route('/movie/<title>', methods=["GET", "POST"])
def movie(title):
    desc = title
    return render_template('movie.html', desc=desc)

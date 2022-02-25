import json
import pprint
import sqlite3
from string import Template

from flask import Flask, jsonify
from flask import request

app = Flask(__name__)


def get_result(query):
    """
    обработка запроса
    :param sql:
    :return:
    """
    with sqlite3.connect('netflix.db') as db:
        db.row_factory = sqlite3.Row
        result = []
        for item in db.execute(query).fetchall():
            result.append(dict(item))

    return result


@app.route('/movie/<title>', methods=["GET"])
def get_title(title: str):
    """
    поиск по названию
    :param title:
    :return:
    """
    query = f'''SELECT *
    from netflix n
    WHERE n.title = {title} and n.date_added = (SELECT max(date added)
    from netflix n
    where n.title = {title})'''
    result = get_result(query)
    return jsonify(result)


@app.route('/years', methods=['GET'])
def get_film_date():
    """
    поиск по диапазону дат
    :return:
    """
    year_from = request.args.get('from')
    year_to = request.args.get('to')
    query = f'''SELECT 
            title,
            release_year
            FROM netflix 
            WHERE release_year BETWEEN {year_from} AND {year_to}
            ORDER BY date_added DESC
    '''
    result = get_result(query)
    return jsonify(result)


@app.route('/rating/<rating>')
def get_rating(rating: str):
    """
    поиск по рейтингу
    :param rating:
    :return:
    """
    children_rating = '"G"'
    family_rating = '"G", "PG", "PG-13"'
    adult_rating = '"R", "NC-17"'
    query_base = Template('''SELECT
                            title,
                            rating,
                            description
                            FROM netflix
                            WHERE rating in ($rating)''')
    if rating == 'children':
        query = query_base.substitute(rating=children_rating)
    elif rating == 'family':
        query = query_base.substitute(rating=family_rating)
    elif rating == 'adult':
        query = query_base.substitute(rating=adult_rating)
    result = get_result(query)
    return jsonify(result)


@app.route('/genre/<genre>', methods=['GET'])
def get_genre(genre: str):
    """
    поиск по жанру
    :param genre:
    :return:
    """
    query = f'''SELECT
                title,
                description
                FROM netflix
                WHERE listed_in like '%{genre}%'
                ORDER BY date_added desc 
                LIMIT 10
    '''
    result = get_result(query)
    return jsonify(result)



def get_actors(actor_one, actor_two):
    """
    поиск по актерам
    :param actor_one:
    :param actor_two:
    :return:
    """
    query = f'''SELECT netflix.cast
                FROM netflix
                WHERE netflix.cast LIKE '%{actor_one}%'
                AND netflix.cast like '%{actor_two}%'
    '''
    result = get_result(query)

    all_casts = [item.get('cast') for item in result]  # собираем всех актеров

    total = []
    actors_list = [item.split(', ') for item in all_casts]  # собираем всех актеров
    cast = [item for item in actors_list]
    for actor in cast:
        if actor == actor_one and actor == actor_two:
            if cast.count(actor) > 2:
                total.append(actor)
            # pprint.pprint(total)
    # pprint.pprint(set(total))
    return str(set(total))


def get_type_year_genre(type, year, genre):
    query = f'''SELECT *
            FROM netflix
            WHERE type = '{type}'
            AND release_year = '{year}'
            AND listed_in LIKE '%{genre}%'
    '''
    result = get_result(query)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)

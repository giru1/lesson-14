import json


def read_json(file):
    """
    читаем файлы json
    """
    with open(file, encoding="utf-8") as f:
        posts = json.load(f)
    return posts





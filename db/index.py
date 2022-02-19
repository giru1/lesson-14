import pprint
import sqlite3

db = sqlite3.connect("C:/PROJECTS/SKYPRO/LESSON-14/db/netflix.db")
cursor = db.cursor()

titles_query = cursor.execute('select `title` from netflix')

titles = [''.join(title) for title in titles_query]


db.commit()
db.close()

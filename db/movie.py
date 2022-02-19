import pprint
import sqlite3

db = sqlite3.connect("C:/PROJECTS/SKYPRO/LESSON-14/db/netflix.db")
cursor = db.cursor()


# task1 = cursor.execute('select `title`, `release_year` from netflix where `release_year`=(select `title`, MAX(`release_year`), MAX(date_added) from netflix)')

def found_for_title(title):
    desc = cursor.execute('select `cast` from netflix where `title`={{ title }}')
    return desc




db.commit()
db.close()


import sqlite3

conn = sqlite3.connect("data/cinemind.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM user_movies")
print(cursor.fetchone())

conn.close()
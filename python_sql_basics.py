import sqlite3

try:
  movieDB = sqlite3.connect("movieDB.db")
  cursor = movieDB.cursor()

  results = cursor.execute("SELECT * FROM directors")

  print(results.fetchone())
  print(results.fetchall())  

except sqlite3.Error as error:
  print('Error occurred - ', error)

finally:
  movieDB.close()
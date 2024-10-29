import sqlite3

try:
    movieDB = sqlite3.connect("movieDB_test.db")
    cursor = movieDB.cursor()

    directors_schema="""
                    CREATE TABLE directors (
                        id INTEGER PRIMARY KEY,
                        name TEXT
                    );
                    """
    results = cursor.execute("DROP TABLE IF EXISTS directors;")
    results = cursor.execute(directors_schema)

    cursor.execute("INSERT INTO directors VALUES (?, ?);", (1, 'Tony Scott'))

    directors_data = [
        (2, "Doug Liman"),
        (3, "Christopher McQuarrie"),
        (4, "Paul Brickman"),
        (5, "Rob Reiner"),
        (6, "Joseph Kosinski"),
        (7, "Steven Spielberg"),
        (8, "Tom Cruise")
    ]
    cursor.executemany("INSERT INTO directors VALUES(?, ?);", directors_data)
    movieDB.commit()
    results = cursor.execute("SELECT * FROM directors")
    print(results.fetchone())
    print(results.fetchall())

except sqlite3.Error as error:
    print('Error occurred - ', error)

finally:
    movieDB.close()
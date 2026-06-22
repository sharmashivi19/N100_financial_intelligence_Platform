import sqlite3


connection = sqlite3.connect(
    "database/nifty100.db"
)


cursor = connection.cursor()


cursor.execute(
    "PRAGMA foreign_keys = ON;"
)


with open(
    "database/schema.sql",
    "r"
) as file:

    schema=file.read()


cursor.executescript(schema)


connection.commit()

connection.close()


print("Database created successfully")
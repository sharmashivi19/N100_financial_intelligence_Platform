import sqlite3


conn = sqlite3.connect(
    "database/nifty100.db"
)

cursor = conn.cursor()


with open(
    "exploratory_queries.sql",
    "r"
) as file:

    sql = file.read()


queries = sql.split(";")

for query in queries:

    if query.strip():

        print("\nRESULT:")
        print("----------------")

        result = cursor.execute(query)

        for row in result.fetchall():
            print(row)


conn.close()
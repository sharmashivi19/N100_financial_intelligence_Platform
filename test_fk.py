from src.ingestion.loader import get_connection


conn=get_connection()


cursor=conn.cursor()


print(
    cursor.execute(
        "PRAGMA foreign_keys;"
    ).fetchone()
)


conn.close()
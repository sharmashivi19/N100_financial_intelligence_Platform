import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv("DB_PATH")


def create_database():

    conn = sqlite3.connect(db_path)

    print("Database created successfully")

    conn.close()


if __name__ == "__main__":
    create_database()
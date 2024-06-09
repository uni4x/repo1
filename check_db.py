import os
import psycopg2


def check_db():
    database_url = os.getenv("DEV_DATABASE_URL")
    conn = psycopg2.connect(database_url)
    print("Database connection successful")


if __name__ == "__main__":
    check_db()

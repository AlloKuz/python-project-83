import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime


def create_connection():
    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL")

    try:
        conn = psycopg2.connect(DATABASE_URL)
    except psycopg2.Error as e:
        print('Unable to connect!\n{0}'.format(e))
    else:
        print('Connected!')

    return conn


def save_data(url):
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute("""INSERT INTO urls (name, created_at) VALUES
                        (%s, %s)""", [url, datetime.now()])


def select_all():
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute("""SELECT name, created_at FROM urls""")
        data = curs.fetchall()
    return data

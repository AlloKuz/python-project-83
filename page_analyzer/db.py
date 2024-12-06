import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
from collections import namedtuple

URLtuple = namedtuple("URLtuple", ["id", "name", "created_at"])


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
    data = []
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute("""SELECT id, name, created_at
                        FROM urls
                        ORDER BY created_at DESC""")
        for el in curs.fetchall():
            data.append(URLtuple._make(el))
    return data


def find_url_by_id(id_):
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute("""SELECT id, name, created_at
                        FROM urls
                        WHERE id = %s""", [str(id_)])
        return URLtuple._make(curs.fetchone())

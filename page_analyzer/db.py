import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
from collections import namedtuple

URLtuple = namedtuple("URLtuple",
                      "id name created_at")
CheckTuple = namedtuple("CheckTuple",
                        "id status_code h1 title description created_at")
URLCheckTuple = namedtuple("URLtuple",
                           "id name last_check response")


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


def select_urls():
    data = []
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute("""SELECT id, name, created_at
                        FROM urls
                        ORDER BY created_at DESC""")
        for el in curs.fetchall():
            data.append(URLtuple._make(el))
    return data


def select_checkinfo():
    data = []
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute("""WITH last_record AS (
                        SELECT url_id, MAX(created_at) last_check
                        FROM url_checks
                        GROUP BY url_id)
                        
                        SELECT urls.id, urls.name, lr.last_check, uc.status_code
                        FROM urls
                        LEFT JOIN last_record as lr
                            ON urls.id=lr.url_id
                        LEFT JOIN url_checks uc ON urls.id=uc.url_id
                        ORDER BY uc.created_at;
                        """)
        for el in curs.fetchall():
            data.append(URLCheckTuple._make(el))
    return data


def select_checks(id_):
    data = []
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute("""SELECT id, status_code, h1,
                               title, description, created_at
                        FROM url_checks
                        WHERE url_id=%s
                        ORDER BY created_at DESC""", [id_])
        for el in curs.fetchall():
            data.append(CheckTuple._make(el))
    return data


def find_url_by_id(id_):
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute("""SELECT id, name, created_at
                        FROM urls
                        WHERE id = %s""", [str(id_)])
        return URLtuple._make(curs.fetchone())


def find_url_by_name(name):
    try:
        with create_connection() as conn, conn.cursor() as curs:
            curs.execute("""SELECT id, name, created_at
                            FROM urls
                            WHERE name = %s""", [name])
            return URLtuple._make(curs.fetchone())
    except Exception as e:
        print(e)
    return False


def save_check(id_, *, status_code=None):
        with create_connection() as conn, conn.cursor() as curs:
            curs.execute("""INSERT INTO url_checks (url_id, created_at, status_code)
                        VALUES (%s, %s, %s)""",
                     [id_, datetime.now(), status_code])

import psycopg2
from psycopg2.extras import DictCursor
import os
import logging


logger = logging.getLogger(__name__)


def create_connection():

    DATABASE_URL = os.getenv("DATABASE_URL")

    try:
        conn = psycopg2.connect(DATABASE_URL,
                                cursor_factory=DictCursor)
        return conn
    except psycopg2.Error as e:
        logger.error(f'Unable to connect!\n{e}')
        raise e


def save_data(url):
    try:
        with create_connection() as conn, conn.cursor() as curs:
            curs.execute("""INSERT INTO urls (name) VALUES
                            (%s)""", [url])
    except psycopg2.Error as e:
        logger.error(f"Connection error! {e}")


def select_urls():
    try:
        with create_connection() as conn, conn.cursor() as curs:
            curs.execute("""SELECT id, name, created_at
                            FROM urls
                            ORDER BY created_at DESC""")
            return curs.fetchall()
    except psycopg2.Error as e:
        logger.error(f"Connection error! {e}")
    return []


def select_last_check_info(id_):
    try:
        with create_connection() as conn, conn.cursor() as curs:
            curs.execute("""SELECT urls.id,
                                   urls.name,
                                   uc.created_at AS last_check,
                                   uc.status_code
                            FROM url_checks AS uc
                            FULL JOIN urls ON uc.url_id=urls.id
                            WHERE urls.id=%s
                            ORDER BY uc.created_at DESC LIMIT 1
                            """, [id_])
            return curs.fetchone()
    except psycopg2.Error as e:
        logger.error(f"Connection error! {e}")
    return {}


def select_checkinfo():
    urls = select_urls()
    checks = []
    for url in urls:
        info = select_last_check_info(url["id"])
        if info:
            checks.append(info)
    return checks


def select_checks(id_):
    try:
        with create_connection() as conn, conn.cursor() as curs:
            curs.execute("""SELECT id, status_code, h1,
                                   title, description, created_at
                            FROM url_checks
                            WHERE url_id=%s
                            ORDER BY created_at DESC""", [id_])
            return curs.fetchall()
    except psycopg2.Error as e:
        logger.error(e)
    return []


def find_url_by_id(id_):
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute("""SELECT id, name, created_at
                        FROM urls
                        WHERE id = %s""", [str(id_)])
        return curs.fetchone()


def find_url_by_name(name):
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute("""SELECT id, name, created_at
                        FROM urls
                        WHERE name = %s""", [name])
        return curs.fetchone()


def save_check(id_, *, status_code=None,
               title=None, h1=None, description=None):
    try:
        with create_connection() as conn, conn.cursor() as curs:
            curs.execute("""INSERT INTO url_checks
                            (url_id,
                             status_code,
                             title,
                             h1,
                             description)
                            VALUES (%s, %s, %s, %s, %s)""",
                         [id_,
                          status_code,
                          title,
                          h1,
                          description])
    except Exception as e:
        logger.error(e)

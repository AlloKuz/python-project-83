import psycopg2
from psycopg2.extras import RealDictCursor
import os
import logging


logger = logging.getLogger(__name__)


def create_connection():
    db_url = os.getenv("DATABASE_URL")
    try:
        conn = psycopg2.connect(db_url,
                                cursor_factory=RealDictCursor)
        return conn
    except psycopg2.Error as e:
        logger.error(f'Unable to connect!\n{e}')
        raise e


def save_url(url):
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute("""INSERT INTO urls (name) VALUES
                        (%s) RETURNING id""", [url])
        return curs.fetchone()


def get_urls():
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute("""SELECT id, name, created_at
                        FROM urls
                        ORDER BY created_at DESC""")
        return curs.fetchall()
    return []


def get_lastchecks():
    sql = """
        WITH most_recent_records AS (
            SELECT url_id, MAX(created_at) AS last_check
            FROM url_checks
            GROUP BY url_id
        )

        SELECT urls.id,
               urls.name,
               uc.status_code,
               uc.created_at AS last_check
        FROM urls
        LEFT JOIN url_checks AS uc
            ON urls.id=uc.url_id
        LEFT JOIN most_recent_records AS mrr
            ON uc.url_id=mrr.url_id
        WHERE mrr.last_check IS NULL OR mrr.last_check=uc.created_at
        ORDER BY urls.created_at DESC;
    """
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute(sql)
        return curs.fetchall()


def get_lastchecks_info():
    checks_info = []
    checks_info = get_lastchecks()
    return checks_info


def get_url_ids():
    sql = """SELECT DISTINCT id FROM urls"""
    with create_connection() as conn, conn.cursor(
            cursor_factory=psycopg2.extensions.cursor) as curs:
        curs.execute(sql)
        data = curs.fetchall()
        return tuple([url_id[0] for url_id in data])
    return []


def get_checks_by_url_id(id_):
    with create_connection() as conn, conn.cursor() as curs:
        curs.execute("""SELECT id, status_code, h1,
                               title, description, created_at
                        FROM url_checks
                        WHERE url_id=%s
                        ORDER BY created_at DESC""", [id_])
        return curs.fetchall()
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

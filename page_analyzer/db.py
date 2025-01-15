import logging
import os

import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


class Repository:
    def __init__(self, db_url=None):
        self.db_url = db_url or os.getenv("DATABASE_URL")

    def create_connection(self):
        return psycopg2.connect(self.db_url)

    def save_url(self, url):
        with self.create_connection() as conn, conn.cursor(
            cursor_factory=RealDictCursor
        ) as curs:
            curs.execute(
                """INSERT INTO urls (name) VALUES (%s) RETURNING id""",
                [url]
            )
            return curs.fetchone()

    def get_urls(self):
        with self.create_connection() as conn, conn.cursor(
            cursor_factory=RealDictCursor
        ) as curs:
            curs.execute(
                """SELECT id, name, created_at
                FROM urls
                ORDER BY created_at DESC"""
            )
            return curs.fetchall()

    def get_urls_with_last_checks(self):
        sql = (
            """
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
                ON urls.id = uc.url_id
            LEFT JOIN most_recent_records AS mrr
                ON uc.url_id = mrr.url_id
            WHERE mrr.last_check IS NULL
                OR mrr.last_check = uc.created_at
            ORDER BY urls.created_at DESC;
            """
        )
        with self.create_connection() as conn, conn.cursor(
            cursor_factory=RealDictCursor
        ) as curs:
            curs.execute(sql)
            return curs.fetchall()

    def get_url_ids(self):
        sql = "SELECT DISTINCT id FROM urls"
        with self.create_connection() as conn, conn.cursor(
            cursor_factory=psycopg2.extensions.cursor
        ) as curs:
            curs.execute(sql)
            data = curs.fetchall()
            return tuple([url_id[0] for url_id in data])

    def get_checks_by_url_id(self, id_):
        with self.create_connection() as conn, conn.cursor(
            cursor_factory=RealDictCursor
        ) as curs:
            curs.execute(
                """SELECT id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id = %s
                ORDER BY created_at DESC""",
                [id_]
            )
            return curs.fetchall()

    def find_url_by_id(self, id_):
        with self.create_connection() as conn, conn.cursor(
            cursor_factory=RealDictCursor
        ) as curs:
            curs.execute(
                """SELECT id, name, created_at
                FROM urls
                WHERE id = %s""",
                [str(id_)]
            )
            return curs.fetchone()

    def find_url_by_name(self, name):
        with self.create_connection() as conn, conn.cursor(
            cursor_factory=RealDictCursor
        ) as curs:
            curs.execute(
                """SELECT id, name, created_at
                FROM urls
                WHERE name = %s""",
                [name]
            )
            return curs.fetchone()

    def save_check(self, url_id, status_code=None, title=None, h1=None,
                   description=None):
        with self.create_connection() as conn, conn.cursor() as curs:
            curs.execute(
                """INSERT INTO url_checks (url_id, status_code, title, h1,
                description) VALUES (%s, %s, %s, %s, %s)""",
                [url_id, status_code, title, h1, description]
            )

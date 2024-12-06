import psycopg2
import os
from dotenv import load_dotenv


def create_connection():
    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL")

    conn = psycopg2.connect(DATABASE_URL)

    return conn

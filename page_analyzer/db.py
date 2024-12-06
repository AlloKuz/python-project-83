import psycopg2
import os
from dotenv import load_dotenv


def create_connection():
    load_dotenv()
    
        DATABASE_URL = os.getenv("DATABASE_URL")

    try:
        conn = psycopg2.connect(DATABASE_URL)
    except:
        print("Cannot connect to database!", file=stderr)
        return None

    return conn

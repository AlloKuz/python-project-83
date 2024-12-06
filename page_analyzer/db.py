import psycopg2
import os
from dotenv import load_dotenv


def create_connection():
    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL")

    keepalive_kwargs = {
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 5,
        "keepalives_count": 5,
    }
    
    try:
        conn = psycopg2.connect(DATABASE_URL, **keepalive_kwargs)
    except psycopg2.Error  as e:
        print('Unable to connect!\n{0}'.format(e))
    else:
        print('Connected!')


    return conn
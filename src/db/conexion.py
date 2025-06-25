import os, psycopg2
from urllib.parse import urlparse

def get_pg_conn():
    return psycopg2.connect(
        host="ep-round-meadow-a5inqt1h-pooler.us-east-2.aws.neon.tech",
        port=5432,
        user="neondb_owner",
        password="npg_cg4vo9OSzfRt",
        database="neondb",
        sslmode="require",
    )
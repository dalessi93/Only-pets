import psycopg2, os
from psycopg2.extras import DictCursor

DB_URL = os.environ.get("DATABASE_URL", "dbname=project2")

def sql_select(sql_query, parameters):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute(sql_query, parameters)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
    

def sql_write(sql_query, parameters):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(sql_query, parameters)
    conn.commit()
    cur.close()
    conn.close()
import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="flask_db",
    user=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS users;")
# TODO: make username unique
cur.execute(
    "CREATE TABLE users (id serial PRIMARY KEY, username varchar (15) NOT NULL, password varchar (15) NOT NULL, date_added timestamp without time zone default (now() at time zone 'utc'));"
)

conn.commit()

cur.close()
conn.close()

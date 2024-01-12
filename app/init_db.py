import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="flask_db",
    user="miles",
    password="miles",
)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS users CASCADE;")
cur.execute("DROP TABLE IF EXISTS scoreboard;")
cur.execute(
    "CREATE TABLE users (user_id SERIAL PRIMARY KEY, \
                         username VARCHAR (15) NOT NULL UNIQUE, \
                         password VARCHAR (255) NOT NULL, \
                         date_added TIMESTAMP without time zone default (now() at time zone 'utc'));"
)

cur.execute(
    "CREATE TABLE base_game_data (id SERIAL PRIMARY KEY, \
                              user_id INT, \
                              title VARCHAR, \
                              time_start TIMESTAMP without time zone default (now() at time zone 'utc'));"
)

cur.execute(
    "CREATE TABLE racer (lap_splits VARCHAR ARRAY)"
)

conn.commit()

cur.close()
conn.close()

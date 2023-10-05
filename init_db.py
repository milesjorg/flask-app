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
    "CREATE TABLE users (user_id SERIAL PRIMARY KEY, \
                         username VARCHAR (15) NOT NULL, \
                         password VARCHAR (15) NOT NULL, \
                         date_added TIMESTAMP without time zone default (now() at time zone 'utc'));"
)

cur.execute(
    "CREATE TABLE scoreboard (game_id SERIAL PRIMARY KEY, \
                              user_id INT, \
                              time_start TIMESTAMP without time zone default (now() at time zone 'utc'), \
                              play_duration INTERVAL, \
                              last_score INT, \
                              high_score INT, \
                              status VARCHAR, \
                              type VARCHAR);"
)

conn.commit()

cur.close()
conn.close()

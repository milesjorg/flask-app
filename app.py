import datetime, os
import psycopg2
from markupsafe import escape
from flask import Flask, render_template, request, flash, url_for, redirect

app = Flask(__name__)
app.config["SECRET_KEY"] = "c0eb487a57f7ab46b2d25c410e60b92a2e7d01c232f4e380"


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user=os.environ["DB_USERNAME"],
        password=os.environ["DB_PASSWORD"],
    )
    return conn

@app.route("/login/", methods=("GET", "POST"))
def login():
    try:
        if request.method == "POST":
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT (username, password) FROM users WHERE username='{request.form['username']}';")
            result = cur.fetchone()[0].split(',')
            user = result[0][1:]
            password = result[1][:-1]
            if password == request.form["password"]:
                print("Login credentials verified")
                return redirect(url_for("home"))
            # TODO: Style error message
            else:
                flash("Invalid credentials", "error")
                return render_template("login.html")
    except TypeError:
        flash("Username/password not recognized")
    return render_template("login.html")


@app.route("/signup/", methods=("GET", "POST"))
def signup():
    print(request)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(request.form["username"])
        print(request.form["password"])

        if not username:
            flash("Field required")
        elif not password:
            flash("Field required")
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("home"))

    return render_template("signup.html")


@app.route("/")
@app.route("/index/")
def home():
    return render_template("index.html", utc_dt=datetime.datetime.utcnow())


@app.route("/capitalize/<word>/")
def capitalize(word):
    return "<h1>{}</h1>".format(escape(word.capitalize()))


@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/arcade/")
def arcade():
    return render_template("arcade.html")

@app.route("/flappybird/")
def flappybird():
    return render_template("flappybird.html")

@app.route("/avalanche/")
def avalanche():
    return render_template("avalanche.html")

@app.route("/slingshot/")
def slingshot():
    return render_template("slingshot.html")

@app.route("/flip/")
def flip():
    return render_template("flip.html")

def create_app():
    app = Flask(__name__)
    app.config["SECRET KEY"] = "c0eb487a57f7ab46b2d25c410e60b92a2e7d01c232f4e380"

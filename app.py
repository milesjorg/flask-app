import datetime, os
import psycopg2
from models.user import User
from markupsafe import escape
from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_session import Session

app = Flask(__name__)
# https://flask-session.readthedocs.io/en/latest/quickstart.html
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=15)
# app.config['SESSION_USE_SIGNER'] = True
app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.config.from_object(__name__)

Session(app)

def get_user(user_id=None, username=None):
    if not user_id and not username:
        return
    if user_id and username:
        return
    conn = get_db_connection()
    cur = conn.cursor()
    if user_id:
        cur.execute(f"SELECT (username, password, user_id) FROM users WHERE user_id={user_id};")
    else:
        cur.execute(f"SELECT (username, password, user_id) FROM users WHERE username='{username}';")

    result = cur.fetchone()[0].split(',')

    username = result[0][1:]
    password = result[1][::]
    user_id = result[2][:-1]
    print(type(user_id))

    user = User(user_id, username, password)
    return user

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
            user = get_user(username=request.form["username"])
            if user.password == request.form["password"]:
                session["user_id"] = user.user_id
                print(session)
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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

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
    user = get_user(user_id=session["user_id"])
    return render_template("index.html", utc_dt=datetime.datetime.utcnow(), user_name=user.username)

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

# def create_app():
#     app = Flask(__name__)
#     app.config["SECRET KEY"] = "c0eb487a57f7ab46b2d25c410e60b92a2e7d01c232f4e380"

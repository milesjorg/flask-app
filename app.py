import datetime, os
import psycopg2
# from models.user import User
from db_models import User, GameData, db
from markupsafe import escape
from flask import Flask, render_template, request, flash, url_for, redirect, session, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

app = Flask(__name__)
# https://flask-session.readthedocs.io/en/latest/quickstart.html
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=15)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://miles:miles@localhost/flask_db"
# app.config['SESSION_USE_SIGNER'] = True
app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]
app.config.from_object(__name__)

Session(app)
db.init_app(app)

def get_user(user_id=None, username=None):
    if not user_id and not username:
        return
    if user_id and username:
        return
    if user_id:
        user = User.query.get(user_id)
    else:
        user = User.query.filter_by(username=username).first()
    print(user)
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
            if user and user.password == request.form["password"]:
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
        existing_user = User.query.filter_by(username=username).first()

        if not username:
            flash("Field required")
        elif not password:
            flash("Field required")
        elif existing_user:
            flash("Username already in use. Please choose a different username")
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            user = get_user(new_user.user_id )
            session["user_id"] = user.user_id
            return redirect(url_for("home"))

    return render_template("signup.html")


@app.route("/")
@app.route("/index/")
def home():
    try:
        user = get_user(user_id=session["user_id"])
        return render_template("index.html", utc_dt=datetime.datetime.utcnow(), user_name=user.username)
    except KeyError:
        return redirect(url_for("login"))
    
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

@app.route("/hourglass/")
def hourglass():
    return render_template("hourglass.html")

@app.route("/store_game_data/", methods=["POST"])
def store_game_data():
    data = request.get_json()
    game_data = GameData(
        user_id = session["user_id"],
        game_name = data["game_name"],
        time_start = data["time_start"],
        # play_duration = data["play_duration"],
        last_score = data["last_score"],
        high_score = data["high_score"],
        # status = data["status"]
    )
    db.session.add(game_data)
    db.session.commit()
    return jsonify(message="Game data stored successfully")

@app.route("/get_user_high_score/")
def get_user_high_score():
    high_score = select([GameData.high_score]).where(
        (GameData.user_id == session["user_id"]) &
        (GameData.game_name == "FlappyBird")
    ).order_by(GameData.high_score).limit(1)
    print(high_score)
    return db.session.execute(high_score).scalar()

# def create_app():
#     app = Flask(__name__)
#     app.config["SECRET KEY"] = "c0eb487a57f7ab46b2d25c410e60b92a2e7d01c232f4e380"

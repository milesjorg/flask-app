import datetime
from config import get_config
from markupsafe import escape
from flask import Flask, session, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_session import Session
from flask_login import LoginManager, login_required, current_user
from app.services.user_service import get_user
from app.routes.auth import auth
from app.routes.common.game import game
from app.extensions import db
from app.models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config('development'))
    print(app.config)

    Session(app)
    db.init_app(app)
    Migrate(app, db)
    # migrate.init_app(app, db)
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"

    app.register_blueprint(auth)
    app.register_blueprint(game)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.route("/dashboard")
    @login_required
    def dashboard():
        try:
            print(session)
            return render_template("dashboard.html", utc_dt=datetime.datetime.utcnow(), user=current_user)
        except KeyError:
            print("got key error")
            return redirect(url_for("auth.login"))
        
    @app.route("/about")
    @login_required
    def about():
        return render_template("about.html")

    @app.route("/arcade")
    @login_required
    def arcade():
        return render_template("arcade.html")
    
    @app.route("/flappybird")
    @login_required
    def flappybird():
        return render_template("flappybird.html")
    
    @app.route("/avalanche")
    @login_required
    def avalanche():
        return render_template("avalanche.html")
    
    @app.route("/slingshot")
    @login_required
    def slingshot():
        return render_template("slingshot.html")

    @app.route("/flip")
    @login_required
    def flip():
        return render_template("flip.html")

    @app.route("/hourglass")
    @login_required
    def hourglass():
        return render_template("hourglass.html")
    
    @app.route("/capitalize/<word>")
    @login_required
    def capitalize(word):
        return "<h1>{}</h1>".format(escape(word.capitalize()))
    
    return app
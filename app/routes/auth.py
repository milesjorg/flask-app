from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.services.user_service.get_user import get_user
from app.models import User, db

auth = Blueprint("auth", __name__)

@auth.route("/")
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user(username=username)
        if user:
            pass_check = user.check_password(password)
            if pass_check:
                login_user(user)
                return redirect(url_for("dashboard"))
        if not username and not password:
            flash("Missing field value")
        else:
            flash("Invalid credentials", "error")
            return render_template("login.html")

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login.html"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        existing_user = User.query.filter_by(username=username).first()

        if not username or not password:
            flash("Field required")
        elif existing_user:
            flash("Username already in use. Be more original")
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("dashboard"))

    return render_template("register.html")

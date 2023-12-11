from flask import Blueprint, render_template

flappybird = Blueprint("flappybird", __name__)

@flappybird.route("/flappybird")
def flappybird():
    return render_template("flappybird.html")

import datetime
from markupsafe import escape
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def home():
    return get_homepage()

@app.route('/capitalize/<word>/')
def capitalize(word):
    return '<h1>{}</h1>'.format(escape(word.capitalize()))

@app.route('/about/')
def about():
    return render_template('about.html')

def get_homepage():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())
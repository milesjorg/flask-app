import datetime
from markupsafe import escape
from flask import Flask, render_template, request, flash, url_for, redirect

app = Flask(__name__)
app.config['SECRET KEY'] = 'c0eb487a57f7ab46b2d25c410e60b92a2e7d01c232f4e380'

accounts = []

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/signup/', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            flash('Field required')
        elif not password:
            flash('Field required')
        else:
            accounts.append({'username': username, 'password': password})
            return redirect(url_for('index'))
        
    return render_template('signup.html')

@app.route('/')
@app.route('/index/')
def home():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())

@app.route('/capitalize/<word>/')
def capitalize(word):
    return '<h1>{}</h1>'.format(escape(word.capitalize()))

@app.route('/about/')
def about():
    return render_template('about.html')

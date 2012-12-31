import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import re
from jinja2 import evalcontextfilter, Markup, escape

# configuration
DATABASE = 'db/quotr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('QUOTR_SETTINGS', silent=True)

# database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('db/schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
            for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

# views
@app.route('/')
def show_quotes():
    quotes = query_db('SELECT id, quote, author FROM quotes ORDER BY id DESC')
    return render_template('show_quotes.html', quotes=quotes)

@app.route('/add', methods=['POST'])
def add_quote():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('INSERT INTO quotes (quote, author) VALUES (?, ?)',
                 [request.form['quote'], request.form['author']])
    g.db.commit()
    flash('New quote successfully added.')
    return redirect(url_for('show_quotes'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Login successful.')
            return redirect(url_for('show_quotes'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logout successful.')
    return redirect(url_for('show_quotes'))

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

if __name__ == '__main__':
    app.run()

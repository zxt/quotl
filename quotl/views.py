from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from quotl import app
from quotl.db import *
from quotl.utils import *

@app.route('/')
@app.route('/quotes/')
@app.route('/quotes/<int:quote_id>')
def show_quotes(quote_id=None):
    if quote_id:
        quote = query_db('SELECT id, quote, author FROM quotes WHERE id = ?', [quote_id], one=True)
        return render_template('show_quote.html', q=quote)
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

from flask import Flask, g

app = Flask(__name__)

import quotl.views
import quotl.db as db

app.config.from_object('quotl.config')
app.config.from_envvar('QUOTL_SETTINGS', silent=True)

@app.before_request
def before_request():
    g.db = db.connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

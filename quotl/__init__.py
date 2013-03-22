from flask import Flask, g
from contextlib import closing

# configuration
DATABASE = 'quotl/db/quotl.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('QUOTL_SETTINGS', silent=True)

import quotl.views
import quotl.db as db

@app.before_request
def before_request():
    g.db = db.connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

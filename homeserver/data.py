# import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# from werkzeug.security import check_password_hash, generate_password_hash

import homeserver.db as dbf

# bp = Blueprint('data', __name__, url_prefix='/data')
bp = Blueprint('data', __name__)


@bp.route('/')
def data():
    db = dbf.get_db()
    rows = db.execute('SELECT * from shower').fetchall()

    s = ""
    for row in rows:
        print(row)
        s = s + str(row['temperature']) + "\n"

    return(s)

@bp.route('/shower', methods=('GET', 'POST'))
def shower():
    db = dbf.get_db()

    if request.method == 'GET':
        rows = db.execute('SELECT * from shower').fetchall()
        return(f'{rows}')

    if request.method == "POST":
        temperature = request.form.get('temperature')

        db.execute(
            "INSERT INTO shower (date, temperature)"
            " VALUES (datetime('now', 'localtime'), ?)",
            (temperature,)
        )        
        
        db.commit()

        return(f'{temperature}')


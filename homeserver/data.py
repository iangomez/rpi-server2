from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import homeserver.db as dbf  # import some useful database functions

# create a "blueprint", i.e., this will hold all the webpages that are about data
# it does not have a url prefix, so our data page is the index of the website
bp = Blueprint('data', __name__)

# index of the site
# shows a dashboard of all logged temperature values
@bp.route('/')
def data():
    db = dbf.get_db() #  open database for this request

    # pull all data from shower
    rows = db.execute('SELECT * from shower').fetchall()

    # print all rows from shower
    s = ""
    for row in rows:
        s = s + str(row['temperature']) + "\n\n"

    return(s)

# GET: this page will show information about the past hour or so. allows us to get specific about our currrent shower
# POST: add the data request to our database
@bp.route('/shower', methods=('GET', 'POST'))
def shower():
    db = dbf.get_db()  # open database for this request

    # display webpage
    if request.method == 'GET':
        # pull latest info out of database
        row = db.execute('SELECT max(id) as latest, date, temperature from shower').fetchone()
        
        t = row['temperature']
        return(f'{t}')

    # responds to our microcontroller sending temperature data
    if request.method == "POST":
        # pull temperature out of POST request
        temperature = request.form.get('temperature')

        # shower db, id automatically increments, datetime is now, temperature is from POST
        db.execute(
            "INSERT INTO shower (date, temperature)"
            " VALUES (datetime('now', 'localtime'), ?)",
            (temperature,)
        )        
        
        db.commit()  # save info in database

        return(f'{temperature}')


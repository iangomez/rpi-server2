from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# import some useful database and data processing functions
import homeserver.db as dbf  
import homeserver.processData as pdf

# create a "blueprint", i.e., this will hold all the webpages that are about data
# it does not have a url prefix, so our data page is the index of the website
bp = Blueprint('data', __name__)

# index of the site
# shows a dashboard of all logged temperature values
@bp.route('/')
def data():
    return pdf.bokehDash(xMax = 2500)

# GET: this page will show information about the past hour or so. allows us to get specific about our currrent shower
# POST: add the data request to our database
@bp.route('/shower', methods=('GET', 'POST'))
def shower():
    db = dbf.get_db()  # open database for this request

    # display webpage
    if request.method == 'GET':
        return pdf.bokehDash(autorefresh=True)
    
    # responds to our microcontroller sending temperature data
    if request.method == "POST":

        # pull temperature out of POST request
        temperature = request.form.get('temperature')

        if temperature:
            temperature = float(temperature)
            print(f'Reported temperature: {temperature} F')

            # shower db, id automatically increments, datetime is now, temperature is from POST
            db.execute(
                "INSERT INTO shower (date, temperature)"
                " VALUES (datetime('now', 'localtime'), ?)",
                (temperature,)
            )        
            
            db.commit()  # save info in database

        return(f'POST received. Temperature = {temperature} F')

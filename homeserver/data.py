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

    bokehOut = pdf.bokehDash()
    if bokehOut:
        html = render_template(
            'dashboard.html',
            plot_script=bokehOut['plot_script'],
            plot_div=bokehOut['plot_div'],
            js_resources=bokehOut['js_resources'],
            css_resources=bokehOut['css_resources'],
        )
    else: 
        html = render_template(
            'dashboard.html',
            emptyDbMessage = "Empty Database"
            )

    return html

# GET: this page will show information about the past hour or so. allows us to get specific about our currrent shower
# POST: add the data request to our database
@bp.route('/shower', methods=('GET', 'POST'))
def shower():
    db = dbf.get_db()  # open database for this request

    # display webpage
    if request.method == 'GET':

        bokehOut = pdf.bokehDash()

        if bokehOut:
            html = render_template(
                'shower.html',
                plot_script=bokehOut['plot_script'],
                plot_div=bokehOut['plot_div'],
                js_resources=bokehOut['js_resources'],
                css_resources=bokehOut['css_resources'],
                autorefresh=True
            )
        else: 
            # using the dashboard html here
            # probably want to standardize the wrapping for the bokeh plots
            html = render_template(
                'dashboard.html',
                emptyDbMessage = "Empty Database"
                )

        return html
    
    # responds to our microcontroller sending temperature data
    if request.method == "POST":

        # pull temperature out of POST request
        temperature = request.form.get('temperature')
        temperature = float(temperature)

        if temperature and temperature > 90:
            print(f'Reported temperature: {temperature} F')

            # shower db, id automatically increments, datetime is now, temperature is from POST
            db.execute(
                "INSERT INTO shower (date, temperature)"
                " VALUES (datetime('now', 'localtime'), ?)",
                (float(temperature),)
            )        
            
            db.commit()  # save info in database

        return(f'POST received. Temperature = {temperature} F')

# purge database of anything under 80F
@bp.route('/purgeDb')
def purgeDb():
    db = dbf.get_db()  # open database for this request
    db.execute("DELETE from shower WHERE temperature<80")
    db.commit()        # save info in database

    return('purge')

@bp.route('/test')
def test():
    return render_template('base.html')
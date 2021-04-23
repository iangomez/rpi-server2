from flask import current_app, g, render_template
from flask.cli import with_appcontext
import homeserver.db as dbf
# bokeh imports
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE

def bokehDash():
    # set up bokeh source
    source = ColumnDataSource()

    # open database and pull everything
    db = dbf.get_db()
    rows = db.execute('SELECT * from shower').fetchall()
    
    # error check data?
    id   = [row['id'] for row in rows]
    date = [row['date'] for row in rows]
    temp = [row['temperature'] for row in rows]

    print(date)

    # make array of shower data for dict
    source.data = dict(
        x = id,
        y = temp,
    )

    # create figure
    fig = figure(plot_height=600, plot_width=720, #x_axis_type='datetime',
                tooltips=[("Date", "@x"), ("Temperature F", "@y")])
    fig.circle(x="x", y="y", source=source, size=8)
    fig.line(x="x", y="y", source=source, line_width=2)

    fig.xaxis.axis_label = "Time"
    fig.yaxis.axis_label = "Temperature"

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    html = render_template(
        'bokeh.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return html

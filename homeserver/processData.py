from flask import current_app, g, render_template
from flask.cli import with_appcontext
import homeserver.db as dbf
# bokeh imports
from bokeh.models import ColumnDataSource, Range1d
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.io import curdoc

import numpy as np


def bokehDash(xMax = None, autorefresh=False):
    # set up bokeh source
    source = ColumnDataSource()

    # open database and pull everything
    db = dbf.get_db()
    rows = db.execute('SELECT * from shower').fetchall()
    
    # error check data?
    id   = [row['id'] for row in rows]
    date = [row['date'] for row in rows]
    temp = [float(row['temperature']) for row in rows]

    xAvg, yAvg = calculateRollingAverage(id, temp, samples=15)

    # make array of shower data for dict
    source.data = dict(
        x = id,
        y = temp,
        date = date,
    )

    # create figure
    fig = figure(plot_height=600, plot_width=720,
                tooltips=[("Date", "@date"), ("Temperature F", "@y"), ("Id", "@x")])
    if xMax:  # if specified x maximum, set on figure
        fig.x_range=Range1d(0, xMax)

    fig.circle(x="x", y="y", source=source, size=1)
    fig.line(x=xAvg, y=yAvg, line_width=2, line_color="red")

    fig.xaxis.axis_label = "Time (seconds)"
    fig.yaxis.axis_label = "Temperature (degrees F)"

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
        autorefresh=autorefresh
    )
    return html

def calculateRollingAverage(x, y, samples=10):
    # reset after max samples taken
    counter = 0
    
    # collect samples to average; resets after max number of samples appended
    avgArr = []
    
    # populate the final rolling average line with these values
    xAvg = [x[0]]
    yAvg = [y[0]]

    # go through each x and y pair
    for i,j in zip(x, y):
        
        # load avgArr with samples
        avgArr.append(j)
        
        # once we have the required number of samples, take the average and reset
        if counter >= samples:
            xAvg.append(i)
            yAvg.append(np.mean(avgArr))
            counter = 0
            avgArr = []
        
        counter += 1

    return xAvg, yAvg
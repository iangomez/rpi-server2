import os
from flask import Flask, render_template

# https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
# application factory way of creating flask site
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'logging.db'),
    )

    print('test config', test_config)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # flask comment: load the test config if passed in
        app.config.from_mapping(test_config)


    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # create database when we make an app
    from . import db
    db.init_app(app)

    # https://flask.palletsprojects.com/en/1.1.x/appcontext/
    # holds useful values that live when the application is alive
    # usually exists as long as a request context exists
    with app.app_context():

        from . import data

        # register our data blueprint and ensure that it's the index of our site
        app.register_blueprint(data.bp)
        app.add_url_rule('/', endpoint='index')

    return app
# services/rsspy/lib/__init__.py


import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(script_info=None):
    """Create the app."""
    # instantiate app
    app = Flask(__name__)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)

    from lib.api.episodes import episodes_blueprint
    app.register_blueprint(episodes_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app

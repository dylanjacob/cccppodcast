# services/rsspy/lib/__init__.py

from flask import Flask, jsonify
from flask_cors import CORS


def create_app(script_info=None):
    """Create the app."""
    # instantiate app
    app = Flask(__name__)

    CORS(app)

    @app.route('/ping', methods=['GET'])
    def ping_pong():
        return jsonify({
            'status': 'success',
            'message': 'pong!'
        })

    @app.shell_context_processor
    def ctx():
        return {'app': app}

    return app

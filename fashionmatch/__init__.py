from flask import Flask

from .home import home

import config

def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False, template_folder="templates")

    with app.app_context():

        app.config.from_object(config.DebugConfig)


        # Register Blueprints
        app.register_blueprint(home.main_bp)

        return app

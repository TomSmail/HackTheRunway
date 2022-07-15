from flask import Flask

from .home import home

def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)

    with app.app_context():

        #app.config.from_object(__name__)


        # Register Blueprints
        app.register_blueprint(home.main_bp)

        return app

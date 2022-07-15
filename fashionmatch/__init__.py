from flask import Flask

from .home import home
from .account import account

import config

#db = SQLAlchemy()

def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False, template_folder="templates", static_folder="static")

    with app.app_context():

        app.config.from_object(config.DebugConfig)


        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(account.account_bp, url_prefix="/account")
        
        return app

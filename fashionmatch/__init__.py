from flask import Flask
import os


from .home import home
from .account import account
from .swap import swap

import config


from sqlalchemy import create_engine, text


def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False,
                template_folder="templates", static_folder="static")

    with app.app_context():

        app.config.from_object(config.DebugConfig)

        from . import db
        
        #db.init_db(app)

        
        
        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(account.account_bp, url_prefix="/account")
        app.register_blueprint(swap.swap_bp, url_prefix="/swap")

        
        # engine = create_engine(os.environ["DATABASE_URL"])
        # conn = engine.connect()

        return app

from flask import Flask


from .home import home
from .account import account
from .swap import swap
from .leaderboard import leaderboard

import config


def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False,
                template_folder="templates", static_folder="static")

    with app.app_context():

        app.config.from_object(config.DebugConfig)

        from . import db # noqa
        # db.init_db(); db.seed_db()
        # # ONLY run this to create the schema afresh
        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(account.account_bp, url_prefix="/account")
        app.register_blueprint(swap.swap_bp, url_prefix="/swap")
        app.register_blueprint(leaderboard.leaderboard_bp, url_prefix="/leaderboard")

        # engine = create_engine(os.environ["DATABASE_URL"])
        # conn = engine.connect()
        return app

from flask import Flask

from .home import home
from .account import account
from .swap import swap

import config

import os
from sqlalchemy import create_engine, text


#tick off received or not

#stepped - including different levels of edge. Thus there could be several edges between people.

#maximum number of cycles.

#show it to all users and get them all to agree

def genGraph():

  numUsers = len(conn.execute(text("SELECT * FROM Users")).fetchall())  
  edges = conn.execute(text("SELECT * FROM User_Has INNER JOIN User_Wants ON User_Has.ArticleID = User_Wants.ArticleID")).fetchall()
  
  graph = [[] for i in range(numUsers)]
  for row in res:
    graph[int(row["User_Has"])].append(int(row["User_Wants"]))
  
  return graph



def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False,
                template_folder="templates", static_folder="static")

    with app.app_context():

        app.config.from_object(config.DebugConfig)


        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(account.account_bp, url_prefix="/account")
        app.register_blueprint(swap.swap_bp, url_prefix="/swap")

        
        engine = create_engine(os.environ["DATABASE_URL"])
        conn = engine.connect()

        return app

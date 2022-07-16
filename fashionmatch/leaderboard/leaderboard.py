from flask import Blueprint, render_template, session
from fashionmatch.auth import ensurelogin
from fashionmatch.db import get_db


lb_bp = Blueprint(
    "leaderboard_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/lstatic'
)


@lb_bp.route("/", methods=["GET"])
@ensurelogin
def home():
    # Fetch Highest Scoring Users
    db, cur = get_db()
    cur.execute('SELECT  firstname, lastname FROM "User" ORDER BY points',)
    resp = cur.fetchall()  
    print(resp)
    return render_template(
        "leaderboard.jinja2",
        response=resp
    )
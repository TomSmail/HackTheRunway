from flask import Blueprint, render_template, session
from fashionmatch.db import get_db


leaderboard_bp = Blueprint(
    "leaderboard_bp", __name__, template_folder="templates",
    static_folder="static", static_url_path='/lstatic'
)


@leaderboard_bp.route("/", methods=["GET"])
def home():
    # Fetch Highest Scoring Users
    db, cur = get_db()
    cur.execute('SELECT  firstname, lastname, points FROM "User" ORDER BY points',)
    resp = cur.fetchall()
    print(resp)
    return render_template(
        "leaderboard.jinja2",
        response=resp
    )

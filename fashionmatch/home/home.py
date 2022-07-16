from flask import Blueprint, render_template, session
from fashionmatch.auth import ensurelogin
from fashionmatch.db import get_db


home_bp = Blueprint(
    "home_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/hstatic'
)


@home_bp.route("/", methods=["GET"])
@ensurelogin
def home():
    # Fetch users items
    db, cur = get_db()
    cur.execute('SELECT  * FROM ("Article" INNER JOIN "User_Has" ON "Article".articleid ="User_Has".articleid) INNER JOIN "User" ON "User_Has".hasuserid="User".userid WHERE "User".email=%s;', (session.get("email",None),))
    resp = cur.fetchall()  
    print(resp)
    return render_template(
        "home.jinja2",
        response=resp
    )

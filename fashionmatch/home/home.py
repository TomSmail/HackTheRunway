from flask import Blueprint, render_template, send_from_directory, session
from flask import current_app as app
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
    cur.execute('SELECT typeofclothing, color, pricerange, condition, locationmade, cotton, imageofitem FROM ("Article" INNER JOIN "User_Has" ON "Article".articleid ="User_Has".articleid) INNER JOIN "User" ON "User_Has".hasuserid="User".userid WHERE "User".email=%s;', (session.get("email", None),))
    has = cur.fetchall()

    cur.execute('SELECT typeofclothing, color, pricerange, condition FROM ("Article" INNER JOIN "User_Wants" ON "Article".articleid ="User_Wants".articleid) INNER JOIN "User" ON "User_Wants".wantsuserid="User".userid WHERE "User".email=%s;', (session.get("email", None),))
    wants = cur.fetchall()

    print(wants)
    #Get num of pending swaps
    uid = (session.get("uid", None))


    cur.execute('SELECT * FROM "Match_Article" INNER JOIN "User_Has" ON "Match_Article".HasID="User_Has".HasID WHERE HasUserID=%s;', (str(uid),))
    amount = len(cur.fetchall())

    return render_template(
        "home.jinja2",
        response=has,
        wants=wants,
        amount=amount
    )


@home_bp.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory("../" + app.config['UPLOAD_FOLDER'], filename, as_attachment=False)

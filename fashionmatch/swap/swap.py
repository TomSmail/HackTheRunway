from flask import Blueprint, Response, make_response, url_for, redirect, request, render_template, flash, session
from flask import current_app as app
import os
from werkzeug.utils import secure_filename

from fashionmatch.db import get_db


swap_bp = Blueprint(
    "swap_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/sstatic'
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'jpg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@swap_bp.route("/", methods=["GET"])
def main():
    return render_template(
        "swap.jinja2",
        PFPs=["https://avatars.githubusercontent.com/u/37508609?s=64&v=4",
              "https://i.stack.imgur.com/56V4z.jpg?s=64&g=1", "https://avatars.githubusercontent.com/u/30555853?s=64&v=4"],
        Names=["Hamish", "John", "Mike"],
        receiver_uname="John",
        sender_uname="Mike",
        locations=[{"lat": 51.5, "long": -0.09},
                   {"lat": 29.7, "long": -5.0}, {"lat": 20.0, "long": 5.0}]
    )


@swap_bp.route("/hasitem", methods=["GET", "POST"])
def hasitem():
    if request.method == 'GET':
        return render_template("hasitem.jinja2")
    if request.method == 'POST':
        db, cur = get_db()

        file = request.files["image"]

        if file.filename == "":
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("..",os.path.join(app.config['UPLOAD_FOLDER'], filename)))   

        colour = request.values.get('colour')
        typeOfItem = request.values.get('type')
        pricerange = request.values.get('pricerange')
        condition = request.values.get('condition') # actually string!
        cotton = request.values.get('cotton')
        locationmade = request.values.get('locationmade')

        cur.execute("""SELECT articleid FROM "Article" WHERE color=%s AND typeofclothing=%s AND pricerange=%s AND condition=%s;""",
                    (colour, typeOfItem, pricerange, condition))
        articles = cur.fetchall()
        if len(articles) != 0:  # article already exists
            print(articles)
            articleid = articles[0]["articleid"]
            userid = session['uid']
            cur.execute("""INSERT INTO "User_Has" (hasuserid, articleid ,imageofitem, cotton, locationmade) VALUES (%s, %s,%s,%s,%s);""",
                        (userid, articleid, filename, cotton, locationmade))
        else:
            cur.execute("""INSERT INTO "Article"(color,typeofclothing,pricerange,condition) VALUES (%s,%s,%s,%s);""",
                        (colour, typeOfItem, pricerange, condition))
            cur.execute("""SELECT articleid FROM "Article" WHERE color=%s AND typeofclothing=%s AND pricerange=%s AND condition=%s;""",
                        (colour, typeOfItem, pricerange, condition))
            articles = cur.fetchall()
            print(articles)
            articleid = articles[0]["articleid"]
            userid = session['uid']
            cur.execute("""INSERT INTO "User_Has" (hasuserid, articleid ,imageofitem,cotton,locationmade) VALUES (%s, %s,%s,%s,%s);""",
                        (userid, articleid, filename, cotton, locationmade))

        return redirect(url_for("home_bp.home"))


@swap_bp.route("/wantsitem", methods=["GET", "POST"])
def add():
    if request.method == 'GET':
        return render_template("add.jinja2")
    elif request.method == 'POST':
        return render_template("add.jinja2")

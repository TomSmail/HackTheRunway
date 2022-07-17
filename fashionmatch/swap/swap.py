from xml.dom.expatbuilder import InternalSubsetExtractor
from flask import Blueprint, Response, make_response, url_for, redirect, request, render_template, flash, session
from flask import current_app as app
import os
from werkzeug.utils import secure_filename

from fashionmatch.db import get_db
from .locateswaps import genGraph, cycleFind
from fashionmatch.auth import ensurelogin


swap_bp = Blueprint(
    "swap_bp", __name__, template_folder="templates", 
    static_folder="static", static_url_path='/sstatic'
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'jpg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@swap_bp.route("/", methods=["GET"])
@ensurelogin
def main():
    # amount = len(cur.fetchall()) Not sure this is needed?
    db, cur = get_db()
    uid = (session.get("uid", None))
    cur.execute('SELECT * FROM "Match_Article" INNER JOIN "User_Has" ON "Match_Article".HasID="User_Has".HasID WHERE HasUserID=%s;', (str(uid),))
    items = cur.fetchall()
    return render_template(
        "allswaps.jinja2",
        number=len(items),
        items=items
    )



@swap_bp.route('/<id>')
@ensurelogin
def swapid(id):
    db, cur = get_db()

    cur.execute('SELECT "Match_Article".hasid,hasuserid,wantsuserid FROM "Match_Article" INNER JOIN "User_Has" ON "Match_Article".HasID="User_Has".HasID INNER JOIN "User_Wants" ON "Match_Article".WantsID="User_Wants".WantsID WHERE matchid=%s;',(id,))
    results = cur.fetchall()
    mapping = {}
    
    for item in results:
        print(item)
        print(session['uid'])
        mapping[item["hasuserid"]] = item["wantsuserid"]
        if item["wantsuserid"] == session['uid']: #This swap is going from item["hasuserid"] to currently logged in user
            sender_id = item["hasuserid"]
            sender_has_id = item["hasid"]
        elif item["hasuserid"] == session['uid']:
            receiver_id = item["wantsuserid"]
            receiver_has_id = item["hasid"]

    cur.execute('SELECT firstname FROM "User" WHERE userid=%s;',(sender_id,));
    sender_uname = cur.fetchall()[0]["firstname"]
    cur.execute('SELECT firstname FROM "User" WHERE userid=%s;',(receiver_id,)); 
    receiver_uname = cur.fetchall()[0]["firstname"]
    cur.execute('SELECT imageofitem FROM "User_Has" WHERE hasid=%s;',(sender_has_id,)); 
    sender_image = cur.fetchall()[0]["imageofitem"]
    cur.execute('SELECT imageofitem FROM "User_Has" WHERE hasid=%s;',(receiver_has_id,)); 
    receiver_image = cur.fetchall()[0]["imageofitem"]
    

    pfps = []
    names = []
    locations = []
    def getNext(userid):
        nonlocal pfps, names
        cur.execute('SELECT firstname,profilepicturelink,coordlat,coordlong FROM "User" WHERE userid=%s;',(userid,));
        record = cur.fetchall()[0]
        pfps.append(record["profilepicturelink"])
        names.append(record["firstname"])
        locations.append({"lat":record["coordlat"],"long":record["coordlong"]})
        return mapping[userid]

    currentUser = list(mapping.keys())[0]
    startUser = list(mapping.keys())[0]
    currentUser = getNext(currentUser)
    while (not(startUser == currentUser)):
        currentUser = getNext(currentUser)
    
    return render_template(
        "swap.jinja2",
        PFPs=pfps,
        Names=names,
        receiver_uname=receiver_uname,
        sender_uname=sender_uname,
        giving_image_url=receiver_image,
        getting_image_url=sender_image,
        locations=locations
    )



    #
    # 
    #IDEALLY WE WANT TO CENTER THE USER SO THEY ARE AT THE MIDDL EOF THE PAGe / MAYB ENOT AN ISSUE 
    #SCROLLBAR?

    


    # startItem = results[0]
    # item = 

    # while item != startItem:

    #     if item["userid"] in participantCounts:

    #     else:
    #         participantCounts.insert(item["userid"])

# @swap_bp.route('/<id>')
# @ensurelogin
# def swapid(id):
    # cur

    # return render_template(
    #     "swap.jinja2",
    #     PFPs=["https://avatars.githubusercontent.com/u/37508609?s=64&v=4",
    #           "https://i.stack.imgur.com/56V4z.jpg?s=64&g=1", "https://avatars.githubusercontent.com/u/30555853?s=64&v=4"],
    #     Names=["Hamish", "John", "Mike"],
    #     receiver_uname="John",
    #     sender_uname="Mike",
    #     locations=[{"lat": 51.5, "long": -0.09},
    #                {"lat": 29.7, "long": -5.0}, {"lat": 20.0, "long": 5.0}]
    # )

# CREATE TABLE "Match_Article" (
# 	MatchArticleID SERIAL PRIMARY KEY NOT NULL,
# 	MatchID INT NOT NULL,
# 	HasID INT REFERENCES "User_Has"(HasID),
# 	WantsID INT REFERENCES "User_Wants"(WantsID) ,
# 	Status VARCHAR(10) NOT NULL
# );


@swap_bp.route("/hasitem", methods=["GET", "POST"])
@ensurelogin
def hasitem():
    if request.method == 'GET':
        return render_template("hasitem.jinja2")
    elif request.method == 'POST':
        db, cur = get_db()

        file = request.files["image"]

        if file.filename == "":
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        colour = request.values.get('colour')
        typeOfItem = request.values.get('type')
        pricerange = request.values.get('pricerange')
        condition = request.values.get('condition')  # actually string!
        cotton = request.values.get('cotton')
        locationmade = request.values.get('locationmade')
        # print(cotton)
        # print(locationmade)

        cur.execute("""SELECT articleid FROM "Article" WHERE color=%s AND typeofclothing=%s AND pricerange=%s AND condition=%s;""",
                    (colour, typeOfItem, pricerange, condition))
        articles = cur.fetchall()
        if len(articles) != 0:  # article already exists
            # print(articles)
            articleid = articles[0]["articleid"]
            userid = session['uid']
            cur.execute("""INSERT INTO "User_Has" (hasuserid, articleid ,imageofitem, cotton, locationmade) VALUES (%s, %s,%s,%s,%s) RETURNING hasid;""",
                        (userid, articleid, filename, cotton, locationmade))
        else:
            cur.execute("""INSERT INTO "Article"(color,typeofclothing,pricerange,condition) VALUES (%s,%s,%s,%s);""",
                        (colour, typeOfItem, pricerange, condition))
            cur.execute("""SELECT articleid FROM "Article" WHERE color=%s AND typeofclothing=%s AND pricerange=%s AND condition=%s;""",
                        (colour, typeOfItem, pricerange, condition))
            articles = cur.fetchall()
            # print(articles)
            articleid = articles[0]["articleid"]
            userid = session['uid']
            cur.execute("""INSERT INTO "User_Has" (hasuserid, articleid ,imageofitem,cotton,locationmade) VALUES (%s, %s,%s,%s,%s) RETURNING hasid;""",
                        (userid, articleid, filename, cotton, locationmade))

        insertedHasID = cur.fetchone()["hasid"]

        getSwaps(None, insertedHasID)
        return redirect(url_for("home_bp.home"))


@swap_bp.route("/wantitem", methods=["GET", "POST"])
@ensurelogin
def wantitem():
    if request.method == 'GET':
        return render_template("wantitem.jinja2")
    elif request.method == 'POST':
        db, cur = get_db()

        colour = request.values.get('colour')
        typeOfItem = request.values.get('type')
        pricerange = request.values.get('pricerange')
        condition = request.values.get('condition')  # actually string!

        cur.execute("""SELECT articleid FROM "Article" WHERE color=%s AND typeofclothing=%s AND pricerange=%s AND condition=%s;""",
                    (colour, typeOfItem, pricerange, condition))
        articles = cur.fetchall()
        if len(articles) != 0:  # article already exists
            # print(articles)
            articleid = articles[0]["articleid"]
            userid = session['uid']
            cur.execute("""INSERT INTO "User_Wants" (wantsuserid, articleid) VALUES (%s, %s) RETURNING wantsid;""",
                        (userid, articleid))
        else:
            cur.execute("""INSERT INTO "Article"(color,typeofclothing,pricerange,condition) VALUES (%s,%s,%s,%s);""",
                        (colour, typeOfItem, pricerange, condition))
            cur.execute("""SELECT articleid FROM "Article" WHERE color=%s AND typeofclothing=%s AND pricerange=%s AND condition=%s;""",
                        (colour, typeOfItem, pricerange, condition))
            articles = cur.fetchall()
            # print(articles)
            articleid = articles[0]["articleid"]
            userid = session['uid']
            cur.execute("""INSERT INTO "User_Wants" (wantsuserid, articleid ) VALUES (%s, %s) RETURNING wantsid;""",
                        (userid, articleid))

        insertedWantsID = cur.fetchone()["wantsid"]

        getSwaps(insertedWantsID, None)
        return redirect(url_for("home_bp.home"))


def getSwaps(addedWantId, addedHasId):
    db, cur = get_db()
    graph = genGraph()
    cycles = cycleFind(graph)
    cycles.sort(key=len)

    cur.execute("""SELECT * FROM "Match_Article";""")
    results = cur.fetchall()
    if len(results) == 0:
        currentCycleID = 0
    else:
        currentCycleID = results[-1]["matchid"]+1

    for cycle in cycles:
        new = False
        for item in cycle:
            # NEEEED TO TEST THIS to ensure it doesn't do it several times.
            if item["HasID"] == addedHasId or item["WantsID"] == addedWantId:
                new = True
        if not(new):
            continue
        for i in range(len(cycle)):
            cur.execute("""INSERT INTO "Match_Article" (MatchID,HasID,WantsID,Status) VALUES (%s,%s,%s,%s);""",
                        (currentCycleID, cycle[i]["HasID"], cycle[i]["WantsID"], "0"))

        currentCycleID += 1

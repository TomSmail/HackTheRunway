from flask import Blueprint, make_response, url_for, redirect, request, render_template, flash, session
from werkzeug.utils import secure_filename

swap_bp = Blueprint(
    "swap_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/sstatic'
)

ALLOWED_EXTENSIONS = {'png','jpg','jpeg','jpg','gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@swap_bp.route("/", methods=["GET"])
def main():
    return render_template(
        "swap.jinja2",
        PFPs=["https://avatars.githubusercontent.com/u/37508609?s=64&v=4","https://i.stack.imgur.com/56V4z.jpg?s=64&g=1","https://avatars.githubusercontent.com/u/30555853?s=64&v=4"],
        Names=["Hamish","John","Mike"],
        receiver_uname="John",
        sender_uname="Mike",
        locations=[{"lat":51.5,"long":-0.09},{"lat":29.7,"long":-5.0},{"lat":20.0,"long":5.0}]
    )


@swap_bp.route("/addhasitem", methods=["GET", "POST"])
def addhasitem():
    if request.method == 'GET':
        return render_template("add.jinja2")
    if request.method == 'POST':
        db, cur = get_db()

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        colour = request.values.get('colour')
        typeOfItem = request.values.get('type')
        pricerange = request.values.get('pricerange')
        condition = request.values.get('condition')
        cotton = request.values.get('cotton')
        locationmade = request.values.get('locationmade')

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        #From the flask documentation

        # If the user does not select a file, the browser submits an
        # empty file without a filename.


        cur.execute("""SELECT articleid FROM "Article" WHERE color='%s' AND typeofclothing='%s' AND pricerange=%s AND condition='%s';""",
                    (colour,typeOfItem,pricerange, condition))
        articles = cur.fetchall()
        if len(articles) != 0: #article already exists
            articleid = articles[0][0]
            userid = session['uid'];
            cur.execute("""INSERT INTO "User_Has" (hasuserid, articleid ,imageofitem,cotton,locationmade) VALUES ('%s', '%s','%s','%s','%s');""",(userid,articleid,filename,cotton,locationmade))
        else:
            cur.execute("""INSERT INTO "Article"(color,typeofclothing,pricerange,condition) VALUES ('%s','%s',%s,'%s');""",
                    (colour,typeOfItem,pricerange,condition))
            cur.execute("""SELECT articleid FROM "Article" WHERE color='%s' AND typeofclothing='%s' AND pricerange=%s AND condition='%s';""",
                        (colour,typeOfItem,pricerange, condition))
            articles = cur.fetchall()
            articleid = articles[0][0]
            userid = session['uid'];
            cur.execute("""INSERT INTO "User_Has" (hasuserid, articleid ,imageofitem,cotton,locationmade) VALUES ('%s', '%s','%s','%s','%s');""",(userid,articleid,filename,cotton,locationmade))

        return redirect(url_for("home_bp.home"))


@swap_bp.route("/wantsitem", methods=["GET", "POST"])
def add():
    if request.method == 'GET':
        return render_template("add.jinja2")
    elif request.method == 'POST':
        return render_template("add.jinja2")

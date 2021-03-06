from fashionmatch.db import get_db
from fashionmatch.auth import ensurelogin


from passlib.hash import argon2
from flask import Blueprint, url_for, redirect, request, render_template, session


account_bp = Blueprint(
    "account_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/astatic',
)


@account_bp.route("/", methods=["GET", "POST"])
@ensurelogin
def home():

    if request.method == 'GET':
        db, cur = get_db()
        cur.execute("""SELECT * FROM "User" WHERE userid=%s;""",
                    (session.get("uid", None),))
        i = cur.fetchone()
        return render_template(
            "updateprofile.jinja2",
            resp=i,
        )
    if request.method == 'POST':
        pass
        print(request.values)
        email = request.values.get('email')
        firstName = request.values.get('firstName')
        lastName = request.values.get('lastName')
        address = request.values.get('address')
        coordlat = request.values.get('coordlat')
        coordlong = request.values.get('coordlong')
        profilepicturelink = request.values.get('profilepicturelink')

        db, cur = get_db()
        cur.execute("""UPDATE "User" SET email= %s,  firstname= %s, lastname= %s, address= %s, coordlat= %s, coordlong= %s, profilepicturelink= %s  WHERE userid=%s;""",
                    (email, firstName, lastName, address, coordlat,
                     coordlong, profilepicturelink, session.get("uid", None),))

        return redirect(url_for("home_bp.home"))


@account_bp.route("/login", methods=["GET", "POST"])  # ! ADD POST!!
def login():
    if request.method == 'GET':
        return render_template(
            "login.jinja2",
        )
    if request.method == 'POST':
        email = request.values.get('email')
        password = request.values.get('password')
        passwordhash = argon2.hash(password)
        # DB
        db, cur = get_db()
        # The comma is very important
        cur.execute(
            'SELECT passwordhash FROM "User" WHERE email = %s;', (email,))
        resp = cur.fetchone()
        if not resp:
            return redirect(url_for("account_bp.login"))
        pwhash = resp["passwordhash"]
        if not argon2.verify(password, pwhash):
            return redirect(url_for("account_bp.login"))
        else:
            db, cur = get_db()

            cur.execute(
                """SELECT userid FROM "User" WHERE email=%s;""", (email,))

            # Session
            session['email'] = email
            session['uid'] = cur.fetchall()[0]["userid"]

            return redirect(url_for("home_bp.home"))


@account_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template(
            "register.jinja2",
        )
    if request.method == 'POST':
        first_name = request.values.get('firstName')
        last_name = request.values.get('lastName')
        email = request.values.get('email')
        password = request.values.get('password')
        # HASHING
        passwordhash = argon2.hash(password)
        # DB
        db, cur = get_db()
        cur.execute('INSERT INTO "User" (email, passwordhash, firstname, lastname) VALUES (%s, %s, %s, %s);',
                    (email, passwordhash, first_name, last_name))

        cur.execute("""SELECT userid FROM "User" WHERE email=%s;""", (email,))

        # Session
        session['email'] = email
        session['uid'] = cur.fetchall()[0]["userid"]
        # return
        return redirect(url_for("home_bp.home"))


@account_bp.route("/logout", methods=["GET"])
@ensurelogin
def logout():
    session.pop('email', None)
    return redirect(url_for("home_bp.home"))

from fashionmatch.db import get_db
from fashionmatch.auth import ensurelogin


from passlib.hash import argon2
from flask import Blueprint, make_response, url_for, redirect, request, render_template, flash, session


account_bp = Blueprint(
    "account_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/astatic', 
)


@account_bp.route("/", methods=["GET"])
@ensurelogin
def home():
    return render_template(
        "account.jinja2",
    )

@account_bp.route("/login", methods=["GET","POST"])  #! ADD POST!!
def login():
    if request.method == 'GET':
        return render_template(
            "login.jinja2",
        )
    if request.method == 'POST':
        email = request.values.get('email')
        password = request.values.get('password')
        passwordhash = argon2.hash(password)
        print(email,passwordhash)
        # DB
        db, cur = get_db()
        cur.execute('SELECT passwordhash FROM "User" WHERE email = %s;', (email,)) # The comma is very important
        resp = cur.fetchone()
        if not resp:
            return redirect(url_for("account_bp.login"))
        pwhash = resp["passwordhash"]
        if not argon2.verify(password, pwhash):           
            return redirect(url_for("account_bp.login"))
        else:
            session['email'] = email
            return redirect(url_for("account_bp.home"))


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
                    (email, passwordhash, first_name, last_name ))

        # Session
        session['email'] = email
        # return
        return redirect(url_for("account_bp.home"))


@account_bp.route("/logout", methods=["GET"])
@ensurelogin
def logout():
    print("Logout")
    session.pop('email', None)
    return redirect(url_for("home_bp.home"))

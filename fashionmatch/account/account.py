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

@account_bp.route("/login", methods=["GET"])  #! ADD POST!!
@ensurelogin
def login():
    return render_template(
        "login.jinja2",
    )

@account_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template(
            "register.jinja2",
        )
    if request.method == 'POST':
        email = request.values.get('email')
        password = request.values.get('password')
        passwordhash = argon2.hash(password)
        db, cur = get_db()
        cur.execute('INSERT INTO "User" (email, passwordhash) VALUES (%s, %s);', (email, passwordhash))
        # Session
        session['email'] = email
        # return
        return make_response("WORKS", 200)


@account_bp.route("/logout", methods=["GET"])
def logout():
    session.pop('email', None)
    return redirect(url_for("account_bp.login"))

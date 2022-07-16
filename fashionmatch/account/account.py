from fashionmatch.db import get_db

from passlib.hash import argon2
from flask import Blueprint, make_response, url_for, redirect, request, render_template, flash, session


account_bp = Blueprint(
    "account_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/astatic', 
)


@account_bp.route("/", methods=["GET"])
def home():
    return render_template(
        "account.jinja2",
    )

@account_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        db, cur = get_db()
        cur.execute('SELECT * FROM usr WHERE id = (%s);', (1,))
        print(cur.fetchone())
        return render_template(
            "register.jinja2",
        )

        
    if request.method == 'POST':
        email = request.values.get('email')
        password = request.values.get('password')
        
        
        print(email, password)
        return make_response("WORKS", 200)


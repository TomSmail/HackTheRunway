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
        return render_template(
            "register.jinja2",
        )
        
    if request.method == 'POST':
        username = request.values.get('email') 
        password = request.values.get('password') 
        print(username,password)
        return make_response("WORKS", 200)

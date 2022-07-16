from flask import Blueprint, url_for, redirect, request, render_template, flash, session
from fashionmatch.auth import ensurelogin


home_bp = Blueprint(
    "home_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/hstatic'
)


@home_bp.route("/", methods=["GET"])
@ensurelogin
def home():
    return render_template(
        "home.jinja2",
    )

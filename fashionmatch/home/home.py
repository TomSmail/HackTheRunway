from flask import Blueprint, url_for, redirect, request, render_template, flash, session


home_bp = Blueprint(
    "home_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/hstatic'
)


@home_bp.route("/", methods=["GET"])
def home():
    return render_template(
        "home.jinja2",
    )

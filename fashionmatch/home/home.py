from flask import Blueprint, url_for, redirect, request, render_template, flash, session


main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/static'
)


@main_bp.route("/", methods=["GET"])
def home():
    return render_template(
        "home.jinja2",
    )

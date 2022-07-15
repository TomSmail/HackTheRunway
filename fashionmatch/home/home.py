from flask import Blueprint, url_for, redirect, request, render_template, flash, session
# from flask import current_app as app
# from flask import render_template


main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/mstatic'
)


@main_bp.route("/", methods=["GET"])
def home():
    return render_template(
        "home.jinja2",
        home_footer="Disclaimer Text",
        fullname=session.get("fullname","Unknown Name")
    )

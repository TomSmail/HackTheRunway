from flask import Blueprint, make_response, url_for, redirect, request, render_template, flash, session


swap_bp = Blueprint(
    "swap_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/sstatic'
)


@swap_bp.route("/", methods=["GET"])
def main():
    return render_template(
        "swap.jinja2",
    )


@swap_bp.route("/swapping", methods=["GET", "POST"])
def swapping():
    if request.method == "GET":
        return render_template(
            "swapping.jinja2",
    )
    elif request.method =="POST":
        approved = request.values.get("approved") # if the user is happy with the swap they will send a bool
        return redirect(url_for("swap_bp.swapped")) # want to redirect to swapped page -- NOT SURE IF THIS WORKS


@swap_bp.route("/swapped", methods=["GET"])
def swapped():
    return render_template(
        "swapped.jinja2",
    )

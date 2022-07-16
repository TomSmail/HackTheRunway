from flask import Blueprint, make_response, url_for, redirect, request, render_template, flash, session


swap_bp = Blueprint(
    "swap_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/sstatic'
)


@swap_bp.route("/", methods=["GET"])
def main():
    return render_template(
        "swap.jinja2",
    )


@swap_bp.route("/swap", methods=["GET", "POST"])
def swap():
    if request.method == "GET":
        return render_template(
            "swapping.jinja2",
    )
    elif request.method =="POST":
        approved = request.values.get("approved") # if the user is happy with the swap they will send a bool
        return approved
        # NOT SURE WHAT TO RETURN
        #return redirect(url_for("swap_bp.swapped"))


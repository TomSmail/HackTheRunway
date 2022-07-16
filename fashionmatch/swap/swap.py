from flask import Blueprint, make_response, url_for, redirect, request, render_template, flash, session


swap_bp = Blueprint(
    "swap_bp", __name__, template_folder="templates", static_folder="static", static_url_path='/sstatic'
)


@swap_bp.route("/", methods=["GET"])
def main():
    return render_template(
        "swap.jinja2",
        PFPs=["https://avatars.githubusercontent.com/u/37508609?s=64&v=4","https://i.stack.imgur.com/56V4z.jpg?s=64&g=1","https://avatars.githubusercontent.com/u/30555853?s=64&v=4"],
        Names=["Hamish","John","Mike"],
        receiver_uname="John",
        sender_uname="Mike",
        locations=[{"lat":51.5,"long":-0.09},{"lat":29.7,"long":-5.0},{"lat":20.0,"long":5.0}]
    )




@swap_bp.route("/additem", methods=["GET", "POST"])
def additem():
    if request.method == 'GET':
        return render_template("additem.jinja2")






"""@swap_bp.route("/swap", methods=["GET", "POST"])
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
"""

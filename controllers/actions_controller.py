from flask import Blueprint, request, session, redirect, render_template
import bcrypt

actions_controller = Blueprint("actions_controller", __name__,)

@actions_controller.route("/home")
def home():
    if session.get('user_id'):
        return render_template("home.html")
    else:
        return redirect("/")

@actions_controller.route("/gallery")
def gallery():
    return render_template("gallery.html")
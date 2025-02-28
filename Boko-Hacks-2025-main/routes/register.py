from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from extensions import db

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        captcha_response = request.form.get("captcha")
        stored_captcha = session.get("captcha_text")

        if not stored_captcha or captcha_response != stored_captcha:
            flash("Invalid CAPTCHA. Please try again.", "error")
            return redirect(url_for("register.register"))

        session.pop("captcha_text", None)

        # prevents user from making multiple accounts with same email
        # email isn't required for logging in 
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("An account with that email already exists. Please choose a different one.", "error")
            return redirect(url_for("register.register"))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for("register.register"))

        new_user = User(username=username)
        new_user.email = email
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login.login"))

    return render_template("register.html")


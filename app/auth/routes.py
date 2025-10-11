from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from . import auth_bp 

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for("admin.index"))
        elif current_user.role == "cobrador":
            return redirect(url_for("collector.index"))
        else:
            return redirect(url_for("client.index"))


    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.authenticate(username, password)
        if user:
            if user.estado != "activo":
                flash("Usuario desactivado. Contacta al administrador.")
                return render_template("auth/login.html")
            login_user(user)
            # Redirige según rol
            if user.role == "admin":
                return redirect(url_for("admin.index"))
            elif user.role == "cobrador":
                return redirect(url_for("collector.index"))
            else:  # cliente
                return redirect(url_for("client.index"))
        flash("Usuario o contraseña incorrectos")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

from __future__ import annotations
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, UserSettings
from .forms import LoginForm, RegisterForm, SettingsForm
import json

bp = Blueprint("auth", __name__, template_folder="templates")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_url = request.args.get("next")
            return redirect(next_url or url_for("main.index"))
        flash("Hibás email vagy jelszó.", "danger")
    return render_template("auth_login.html", form=form)

@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("Ez az email már foglalt.", "warning")
            return render_template("auth_register.html", form=form)
        u = User(email=form.email.data.lower(), password_hash=generate_password_hash(form.password.data))
        db.session.add(u)
        db.session.flush()
        # alap settings
        s = UserSettings(user_id=u.id)
        db.session.add(s)
        db.session.commit()
        flash("Sikeres regisztráció! Jelentkezz be.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth_register.html", form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    s = current_user.settings or UserSettings(user_id=current_user.id)
    form = SettingsForm(
        default_list_id=s.default_list_id,
        default_priority=str(s.default_priority),
        default_status=s.default_status,
        default_due_days=s.default_due_days,
        quick_add_fields=s.quick_add_fields or '["title","list_id"]'
    )
    if form.validate_on_submit():
        s.default_list_id = form.default_list_id.data
        s.default_priority = int(form.default_priority.data)
        s.default_status = form.default_status.data
        s.default_due_days = form.default_due_days.data or 0
        # valid JSON?
        text = (form.quick_add_fields.data or "").strip()
        if text:
            try:
                data = json.loads(text)
                if not isinstance(data, list):
                    raise ValueError("A quick_add_fields nem lista.")
                s.quick_add_fields = json.dumps(data, ensure_ascii=False)
            except Exception as e:
                flash(f"quick_add_fields hiba: {e}", "danger")
                return render_template("settings.html", form=form)
        else:
            s.quick_add_fields = None

        if current_user.settings is None:
            db.session.add(s)
        db.session.commit()
        flash("Beállítások mentve.", "success")
        return redirect(url_for("auth.settings"))
    return render_template("settings.html", form=form)

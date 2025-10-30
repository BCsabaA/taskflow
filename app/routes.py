from __future__ import annotations
from flask import Blueprint, render_template, jsonify
import sys
import flask
import sqlite3


bp = Blueprint("main", __name__)


def _collect_sysinfo(app):
    db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
    db_path = db_uri.replace("sqlite:///","") if db_uri.startswith("sqlite") else db_uri
    return {
        "python": sys.version.split()[0],
        "flask": flask.__version__,
        "sqlite": sqlite3.sqlite_version,
        "db_path": db_path,
        "debug": app.debug,
    }


@bp.get("/")
def index():
    return render_template("index.html", app_name="TaskFlow", version="0.1.0")
    # return "INDEX OK", 200, {"Content-Type": "text/plain; charset=utf-8"}

@bp.get("/healthz")
def healthz():
    # TODO: ide jön a valódi ellenőrzés (DB ping, verziók), most minimal
    return jsonify({"status": "ok"})

@bp.get("/about")
def about():
    from flask import current_app
    info = _collect_sysinfo(current_app)
    return render_template("about.html", info=info, version="0.1.0")
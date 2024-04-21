from flask import Blueprint, abort
from flask.templating import render_template
from flask_login.utils import login_required
from ..utils import get_bool_env
from ..database.db import (
    AuslagenKategorie
)


auslagen_site = Blueprint("auslagen_site", __name__, url_prefix="/auslagen")

@auslagen_site.before_request
def before():
    if not get_bool_env("KP_AUSLAGEN_AKTIV", True):
        abort(501)  # Feature not enabled -> abort with Not Implemented

@auslagen_site.route("/")
@login_required
def auslagen_uebersicht():
    kategorienListe = AuslagenKategorie.query.all()
    return render_template("auslagen/auslagen.html", kategorienListe=kategorienListe)

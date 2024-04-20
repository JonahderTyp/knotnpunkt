from flask import Blueprint
from flask.templating import render_template
from flask_login.utils import login_required
from ..database.db import (
    AuslagenKategorie
)


auslagen_site = Blueprint("auslagen_site", __name__, url_prefix="/auslagen")


@auslagen_site.route("/")
@login_required
def auslagen_uebersicht():
    kategorienListe = AuslagenKategorie.query.all()
    return render_template("auslagen/auslagen.html", kategorienListe=kategorienListe)

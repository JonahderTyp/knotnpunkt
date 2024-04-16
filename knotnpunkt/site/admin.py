from flask import Blueprint, abort
from flask.templating import render_template
from flask_login import current_user
from flask_login.utils import login_required
from ..database.db import Benutzer


admin_site = Blueprint("admin_site", __name__, url_prefix="/admin")


@admin_site.before_request
@login_required
def auth():
    usr: Benutzer = current_user
    if not usr.rechte().get("einstellungenLesen", False):
        abort(401)
        # return redirect(url_for('site.login')) # alternativ zum Fehlercode
    pass


@admin_site.route("/einstellungen")
@login_required
def einstellungen():
    return render_template('admin/server_einstellungen.html')

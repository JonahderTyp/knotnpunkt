from flask import Blueprint
from flask.templating import render_template
from flask_login.utils import login_required


admin_site = Blueprint("admin_site", __name__, url_prefix="/admin")


@admin_site.route("/einstellungen")
@login_required
def einstellungen():
    return render_template('admin/server_einstellungen.html')

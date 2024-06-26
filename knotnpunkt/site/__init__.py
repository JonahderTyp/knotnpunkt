from datetime import date
from flask import request, Blueprint
from flask.helpers import url_for
from flask.templating import render_template
from flask_login import current_user
from flask_login.utils import login_required, login_user, logout_user
from sqlalchemy import desc
from werkzeug.utils import redirect
from ..database import db
from ..database.db import (
    Benutzer,
    Material,
    Ausleihe,
)
from ..utils import get_bool_env
from .material import material_site
from .user import user_site
from .admin import admin_site
from .auslagen import auslagen_site

site = Blueprint("site", __name__, template_folder="templates")
site.register_blueprint(material_site)
site.register_blueprint(user_site)
site.register_blueprint(admin_site)
site.register_blueprint(auslagen_site)


@site.context_processor
def inject_views():
    if not current_user.is_authenticated:
        return {}
    usr: Benutzer = current_user
    views = []
    for view in [i.lower() for i in usr.views()]:
        if "kalender" in view:
            views.append({"name": "Kalender", "url": url_for("site.kalender")})
        if "benutzer" in view:
            views.append(
                {"name": "Benutzer", "url": url_for("site.user_site.benutzer")})
        if "material" in view:
            views.append({"name": "Material", "url": url_for(
                "site.material_site.material")})
        if "einstellungen" in view:
            views.append({"name": "Einstellungen", "url": url_for(
                "site.admin_site.einstellungen")})
    if get_bool_env("KP_AUSLAGEN_AKTIV", True):
        views.append({"name": "Auslagen", "url": url_for(
            "site.auslagen_site.auslagen_uebersicht")})
    return {"views": views}


@site.route('/')
def redirectToLogin():
    return redirect(url_for('site.login'))


@site.route("/login", methods=['GET', 'POST'])
def login():
    error_msg = ""
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))
    if request.args.get("newPassword"):
        error_msg = "Bitte melde dich mit deinem neuen Passwort an."
    if request.method == 'POST':
        user = Benutzer.query.get(request.form['benutzername'])
        if user:
            if user.passwort == request.form.get('passwort'):
                login_user(user, remember=True)
                return redirect(url_for("site.user_site.profil", benutzername=user.benutzername, initialLogin=True))
            elif user.check_passwort(request.form['passwort']):
                login_user(user, remember=True)
                return redirect(url_for('site.home'))
            else:
                error_msg = 'Ungültige Anmeldedaten. Bitte überprüfe Benutzername und Passwort.'
        else:
            error_msg = 'Ungültige Anmeldedaten. Bitte überprüfe Benutzername und Passwort.'
    return render_template('login.html', error=error_msg)


@site.route('/logout', methods=['GET'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('site.login'))


@site.route('/home')
@login_required
def home():
    ausleihen = Ausleihe.query.filter_by(
        ersteller_benutzername=current_user.benutzername).order_by(desc(Ausleihe.ts_von)).all()
    ausleihen_filtered_future = []
    ausleihen_filtered_past = []
    stats_list = []
    for a in ausleihen:
        materialien = []
        for m in a.materialien.split(","):
            materialien.append(Material.query.filter_by(idMaterial=m).first())
            stats_list.append(m)
        ausleihe = {'empfaenger': a.empfaenger, "ts_von": a.ts_von,
                    "ts_bis": a.ts_bis, "materialien": materialien}
        if a.ts_von > date.today():
            ausleihen_filtered_future.append(ausleihe)
        else:
            ausleihen_filtered_past.append(ausleihe)
    stats_dict = dict()
    stats_dict1 = dict()
    max_value = 0
    if len(stats_list) > 0:
        for i in stats_list:
            stats_dict[str(i)] = stats_dict.get(str(i), 0)+1
        materialien = Material.query.all()
        for m in materialien:
            stats_dict1[m.name] = stats_dict.get(
                str(m.idMaterial), 0) / len(stats_list)*100
        max_value = max(stats_dict1.values())
    return render_template('home.html', ausleihen_zukunft=ausleihen_filtered_future[:3], ausleihen_alt=ausleihen_filtered_past[:3], stats=stats_dict1, max=max_value)


@site.route("/kalender")
@login_required
def kalender():
    return render_template('kalender.html')

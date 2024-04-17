"""The api submodule contains routes that dont render templates.
"""
from os import environ
from flask import Blueprint
from .material import materialBlueprint
from .auslagen import auslagen_routes

api = Blueprint("api", __name__, template_folder="templates",
                url_prefix="/api")

api.register_blueprint(materialBlueprint)
if environ.get("KP_AUSLAGEN_AKTIV", True):
    api.register_blueprint(auslagen_routes)
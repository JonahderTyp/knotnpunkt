"""The api submodule contains routes that dont render templates.
"""
from os import environ
from flask import Blueprint
from .material import materialBlueprint
from .auslagen import auslagen_routes

apiv1 = Blueprint("apiv1", __name__, template_folder="templates",
                url_prefix="/api/v1")

apiv1.register_blueprint(materialBlueprint)
if environ.get("KP_AUSLAGEN_AKTIV", True):
    apiv1.register_blueprint(auslagen_routes)
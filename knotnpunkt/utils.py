import os
import humanize as hu
from sqlalchemy import desc
import json
from datetime import datetime as dt
from datetime import date
from .database.db import (
    Ausleihe,
    Material,
)


def convertTime(datetime):
    _t = hu.i18n.activate("de_DE")
    return hu.naturaltime(dt.now()-dt.strptime(datetime.get('zuletztGescannt'), '%Y-%m-%d %H:%M'))


def checkverfuegbarkeit(materialien):
    dict_verfuegbar = {}
    ausleihen = Ausleihe.query.order_by(desc(Ausleihe.ts_von)).all()
    for m in materialien:
        if m.Eigenschaften.get('zaehlbar', False):
            dict_verfuegbar[m.idMaterial] = m.Eigenschaften.get('anzahl', 1)
        else:
            dict_verfuegbar[m.idMaterial] = True
        for a in ausleihen:
            if int(m.idMaterial) in [int(x) for x in a.materialien.split(",") if x.isdigit()]:
                if a.ts_von <= date.today() <= a.ts_bis:
                    if m.Eigenschaften.get('zaehlbar', False) == False:
                        dict_verfuegbar[m.idMaterial] = False
                    else:
                        dict_verfuegbar[m.idMaterial] = dict_verfuegbar[m.idMaterial] - 1
    return dict_verfuegbar


def get_ausleihen_fuer_material(materialien: list[Material] | str) -> list:
    """Abfrage nach den Ausleihen in der Datenbank, die bestimmte Materialien
    enthalten

    Args:
        materialien (list[Material] | str): Liste von Material-Klassen oder einzelne id

    Returns:
        list: Enthält ein Tupel für jedes Material: z. B. 
        [(<Material 1>, [<Ausleihe 1>, <Ausleihe 2>]), (<Material 2>, [<Ausleihe 1>]),
    """
    if isinstance(materialien, str):
        materialien = Material.query.filter_by(idMaterial=material).all()
    elif not isinstance(materialien, list):
        return None
    ausleihen = [(a, a.materialien.split(",")) for a in Ausleihe.query.all()]
    if ausleihen == []:
        return None
    result = {m.idMaterial: [a[0] for a in ausleihen if str(
        m.idMaterial) in a[1]] for m in materialien}
    return result


def allowed_file(filename):
    """Test if uploaded images have legit filenames, Used by Auslagen
    image upload.

    Args:
        filename (str): Filename to be tested

    Returns:
        bool: True if filename is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ["png", "jpg", "jpeg", "gif"]


def get_bool_env(var_name: str, default: bool | None = False) -> bool | ValueError | None:
    """ 
    Retrieve an environment variable and convert it to a boolean.

    This function fetches the value of an environment variable and attempts to interpret it as a boolean. 
    Common boolean string representations such as 'true', '1', 't', 'y', 'yes', 'on' for True, and 'false', 
    '0', 'f', 'n', 'no', 'off' for False are supported. If the value is not one of these, or if it's missing
    and no default is provided, the function raises a ValueError.

    Args:
        var_name (str): The name of the environment variable to retrieve.
        default (bool | None): The default value to return if the environment variable is not set. 
            If `None`, it indicates no default value is provided.

    Returns:
        bool | None: The boolean value of the environment variable or the default value if the variable is not set.

    Raises:
        ValueError: If the environment variable's value cannot be interpreted as a boolean and no default is provided.

    Example:
        >>> get_bool_env('FEATURE_ENABLED')
        True
        >>> get_bool_env('INVALID_VALUE')
        ValueError: Env var could not be parsed
    """
    value = os.getenv(var_name)
    if value is None:
        return default
    if value.lower() in ['true', '1', 't', 'y', 'yes', 'on']:
        return True
    if value.lower() in ['false', '0', 'f', 'n', 'no', 'off']:
        return False
    raise ValueError("Env var could not be parsed")

"""This module has some utility functions"""

from typing import Set


def allowed_file(file_name: str, allowed_extensions: Set[str]) -> bool:
    """
    Check if file has allowed extension from provided Set

    Parameters
    ----------
    file_name, str
        path to file which should be checked
    allowed_extensions, Set[str]
        Set of allowed extensions

    Returns
    -------
    bool
        True - if provided file has allowed extensions
        False - otherwise
    """
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in allowed_extensions

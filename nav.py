import typing as t
from typing import List, Tuple
from flask import url_for, Blueprint

_nav_titles = {}


def register_title(title: str, *, blueprint: t.Optional[Blueprint] = None) -> t.Callable:
    """Register a title for the specified route function.

    This title will be displayed in the navigation bar.
    """
    def _reg(func):
        endpoint = func.__name__
        if blueprint is not None:
            endpoint = f"{blueprint.name}.{endpoint}"
        _nav_titles[endpoint] = title
        return func
    return _reg


def get_title(endpoint: str) -> t.Optional[str]:
    """Get a title assigned to the specified endpoint.

    ``endpoint`` is a ``flask.url_for``-compatible endpoint
    identifier. Refer to the Flask documentation for more details.
    """
    return _nav_titles.get(endpoint)


def make_path(endpoints: List[str]) -> List[Tuple[str, str]]:
    """Generate a list of ``(endpoint_url, endpoint_title)`` pairs for use in the navigation bar.

    In order to render the navigation bar, the list returned by this
    function must be passed to the template renderer in the ``nav``
    argument. The template must include the ``_nav.html`` subtemplate
    as well.
    """
    return [(url_for(e), _nav_titles[e]) for e in endpoints]

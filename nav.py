"""
This module contains support functions for rendering the navigation bar.
The navigation bar lives in the ``_nav.html`` template. This template expects
two parameters: ``page_title`` for displaying the current page's title and
``nav`` for displaying the navigation path (also known as breadcrumbs).
The ``nav`` parameter is a list of (endpoint_url, endpoint_title) pairs. It
can be generated with the ``make_nav`` function, provided you've registered
the titles for all endpoints you want to use with the ``register_title``
decorator first.
"""

from typing import List, Tuple, Optional, Callable
from flask import url_for, Blueprint

_nav_titles = {}


def register_title(title: str, *, blueprint: Optional[Blueprint] = None) -> Callable:
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


def get_title(endpoint: str) -> Optional[str]:
    """Get a title assigned to the specified endpoint.

    If no title is assigned, the return value is None.

    Parameters
    ----------
    endpoint: str
        A ``flask.url_for``-compatible endpoint identifier.
        Refer to the Flask documentation for more details.
    """
    return _nav_titles.get(endpoint)


def make_path(endpoints: List[str]) -> List[Tuple[str, str]]:
    """Generate a list of ``(endpoint_url, endpoint_title)`` pairs for use in the navigation bar.

    In order to render the navigation bar, the list returned by this
    function must be passed to the template renderer in the ``nav``
    argument. The template must include the ``_nav.html`` subtemplate
    as well.

    Parameters
    ----------
    endpoints: List[str]
        A list of ``flask.url_for``-compatible endpoint identifiers.
        Each endpoint should have its title registered using the
        ``register_title`` decorator.
    """
    return [(url_for(e), _nav_titles[e]) for e in endpoints]

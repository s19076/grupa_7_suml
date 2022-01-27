import typing as t
from typing import List, Tuple
from flask import url_for, Blueprint

_nav_titles = {}


def register_title(title: str, *, blueprint: t.Optional[Blueprint] = None) -> t.Callable:
    def _reg(func):
        endpoint = func.__name__
        if blueprint is not None:
            endpoint = f"{blueprint.name}.{endpoint}"
        _nav_titles[endpoint] = title
        return func
    return _reg
    

def get_title(endpoint: str) -> t.Optional[str]:
    return _nav_titles.get(endpoint)


def make_path(endpoints: List[str]) -> List[Tuple[str, str]]:
    return [(url_for(e), _nav_titles[e]) for e in endpoints]

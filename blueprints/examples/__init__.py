"""Blueprints endopits for `/examples`"""
from flask import Blueprint, render_template

import nav

blueprint = Blueprint("examples", __name__, url_prefix="/examples")
MAX_EXAMPLE_ID = 15


@blueprint.route("/")
@nav.register_title("Examples", blueprint=blueprint)
def get_examples():
    """
    Render a template for `/examples` endpoint
    """
    return render_template(
        "examples.html",
        page_title="Examples",
        nav=nav.make_path(["index.get_home"]),
        max_example_id=MAX_EXAMPLE_ID,
    )


@blueprint.route("/<int:example_id>", methods=["GET"])
def get_example(example_id: int):
    """
    Render a template for `/examples/<int:example_id>`

    Parameters
    ----------
    example_id: int
        id for example, should be from 0-15 range
    """
    if example_id < 0 or example_id > MAX_EXAMPLE_ID:
        return render_template("404.html")

    return render_template(
        "example.html",
        page_title=example_id,
        nav=nav.make_path(["index.get_home", "examples.get_examples"]),
        example_id=example_id,
        max_example_id=MAX_EXAMPLE_ID,
    )

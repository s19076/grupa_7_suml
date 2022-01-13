# blueprints/endpoints/__init__.py
from flask import Blueprint, render_template, request

blueprint = Blueprint("examples", __name__, url_prefix="/examples")


@blueprint.route("/<int:example_id>", methods=["GET"])
def get_example(example_id):
    if example_id < 0 or example_id > 15:
        return render_template("404.html")
    if example_id == 15:
        return render_template("example_last.html", example_id=example_id)
    if example_id == 0:
        return render_template("example_first.html", example_id=example_id)
    return render_template("example.html", example_id=example_id)


# blueprints/endpoints/__init__.py
from flask import Blueprint, render_template, request

blueprint = Blueprint("examples", __name__, url_prefix="/examples")
MAX_EXAMPLE_ID = 15

@blueprint.route("/<int:example_id>", methods=["GET"])
def get_example(example_id):
    if example_id < 0 or example_id > MAX_EXAMPLE_ID:
        return render_template("404.html")

    return render_template(
        "example.html",
        example_id = example_id,
        max_example_id = MAX_EXAMPLE_ID,
    )


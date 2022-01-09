# blueprints/endpoints/__init__.py
from flask import Blueprint, render_template

blueprint = Blueprint("index", __name__, url_prefix="/")


@blueprint.route("home")
def get_home():
    return render_template("home.html")

@blueprint.route("examples")
def get_examples():
    return render_template("examples.html")
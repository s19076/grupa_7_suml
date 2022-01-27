# blueprints/endpoints/__init__.py
from flask import Blueprint, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
from config import *
from utils import allowed_file

blueprint = Blueprint("index", __name__, url_prefix="/")


@blueprint.route("home")
def get_home():
    return render_template("home.html")


@blueprint.route("examples")
def get_examples():
    return render_template("examples.html")


@blueprint.route("upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return render_template("upload_photo.html")

        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)

            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return render_template(
                "restore_image.html",
                path_original = f"uploads/{filename}",
                path_restored = f"restored/{filename}",
            )
    return render_template("upload_photo.html")

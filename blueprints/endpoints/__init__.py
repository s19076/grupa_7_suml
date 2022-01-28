# blueprints/endpoints/__init__.py
from flask import Blueprint, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
from config import *
from utils import allowed_file
from model import restore_image
import nav

blueprint = Blueprint("index", __name__, url_prefix="/")


@blueprint.route("/")
@nav.register_title("Index", blueprint=blueprint)
def get_index():
    return redirect("home")

@blueprint.route("home")
@nav.register_title("Home", blueprint=blueprint)
def get_home():
    return render_template("home.html", page_title = "Home")


@blueprint.route("upload", methods=['GET', 'POST'])
@nav.register_title("Upload photo", blueprint=blueprint)
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file is None or file.filename == '':
            return render_template(
                "upload_photo.html",
                page_title = "Upload photo",
                nav = nav.make_path(["index.get_home"]),
                error = "You must select a file",
            )

        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)

            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)

            file.save(os.path.join(UPLOAD_FOLDER, filename))
            restore_image(os.path.join(UPLOAD_FOLDER, filename))
            return render_template(
                "restore_image.html",
                page_title = "Restore image",
                nav = nav.make_path(["index.get_home", "index.upload_file"]),
                path_original = f"uploads/{filename}",
                path_restored = f"restored/{filename.split('.')[0]}_restored.{filename.split('.')[1]}",
            )
    return render_template(
        "upload_photo.html",
        page_title = "Upload photo",
        nav = nav.make_path(["index.get_home"]),
    )

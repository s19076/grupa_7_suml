import subprocess
import os

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
           
def get_face_model():
    if not os.path.exists(path = "model/face_model/GFPGANCleanv1-NoCE-C2.pth"):
        subprocess.run(["wget",
                        "https://github.com/TencentARC/GFPGAN/releases/download/v0.2.0/GFPGANCleanv1-NoCE-C2.pth",
                        "-P",
                        "model/face_model"])

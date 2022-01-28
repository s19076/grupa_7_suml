"""Config file, contains configuration values for project"""

ALLOWED_EXTENSIONS = {"jpg", "png", "img", "jpeg"}
UPLOAD_FOLDER = "static/uploads"
RESTORE_FOLDER = "static/restored"

# MODEL PARAMETERS
BACKGROUND_MODEL_NAME = "realesrgan"
UPSCALE = 2
ARCH = "clean"
CHANNEL = 2
ALIGNED = False
ONLY_CENTER_FACE = False
PASTE_BACK = True
EXTENSION = "auto"

# main.py
from flask import Flask
from utils import get_face_model
from blueprints.endpoints import blueprint as endpoints
from blueprints.examples import blueprint as example

app = Flask(__name__)
app.config["SECRET_KEY"] = "TOKEN"

app.register_blueprint(endpoints)
app.register_blueprint(example)

get_face_model()

if __name__ == "__main__":
    app.run(debug = True)

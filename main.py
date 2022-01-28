# main.py
from flask import Flask
from model import download_models
from blueprints.endpoints import blueprint as endpoints
from blueprints.examples import blueprint as example

app = Flask(__name__)
app.config["SECRET_KEY"] = "TOKEN"

app.register_blueprint(endpoints)
app.register_blueprint(example)

download_models()

if __name__ == "__main__":
    app.run(debug = True)

"""Main"""
from flask import Flask
from blueprints.endpoints import blueprint as endpoints
from blueprints.examples import blueprint as example
from model import download_models

app = Flask(__name__)
app.config["SECRET_KEY"] = "TOKEN"

app.register_blueprint(endpoints)
app.register_blueprint(example)

download_models()

if __name__ == "__main__":
    app.run(debug=True)

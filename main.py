# main.py
from flask import Flask
# from blueprints.documented_endpoints import blueprint as documented_endpoint
from blueprints.endpoints import blueprint as endpoints
from blueprints.examples import blueprint as example

app = Flask(__name__)
app.config["SECRET_KEY"] = "TOKEN"

# app.register_blueprint(documented_endpoint)
app.register_blueprint(endpoints)
app.register_blueprint(example)

if __name__ == "__main__":
    app.run(debug = True)
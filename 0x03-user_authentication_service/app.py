#!/usr/bin/env python3
""" A simple flask app"""
from flask import jsonify, Flask

app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def index():
    """return the index page"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

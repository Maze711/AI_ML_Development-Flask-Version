from flask import Flask, jsonify, Blueprint
import requests
from users_api import api_get

app = Flask(__name__)
app.register_blueprint(api_get)

if __name__ == '__main__':
    app.run(debug=True)
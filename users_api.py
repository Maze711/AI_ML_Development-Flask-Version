from flask import Flask, jsonify, Blueprint
import requests

api_get = Blueprint("get_users", __name__)

@api_get.route('/api_get', methods=['GET', 'POST'])
def get_users():
    try:
        users_url = "https://jsonplaceholder.typicode.com/users"
        response = requests.get(users_url)

        if response.status_code == 200:
            users = response.json()
            return jsonify([user["address"] 
                            for user in users]), response.status_code 
        else:
            return jsonify({"message": "Failed to fetch data"}), response.status_code
    except Exception as e:
        return jsonify({"message": "Failed to fetch data"}), 500
    
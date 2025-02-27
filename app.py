from flask import Flask, jsonify
import requests

app = Flask(__name__)
@app.route('/api_get', methods=['GET', 'POST'])
def api_get():
    try:
        users_url = "https://jsonplaceholder.typicode.com/users"
        response = requests.get(users_url)

        if response.status_code == 200:
            users = response.json()
            return jsonify({"address": user["address"]
                            for user in users
                            }), response.status_code
        else:
            return jsonify({"message": "Failed to fetch data"}), response.status_code
    except Exception as e:
        return jsonify({"message": "Failed to fetch data"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
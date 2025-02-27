from flask import Flask
from api.users_api import api_get
from api.study_api import get_study

app = Flask(__name__)
#app.register_blueprint(api_get)
app.register_blueprint(get_study)

if __name__ == '__main__':
    app.run(debug=True)
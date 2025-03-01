from flask import Flask
import os
from config.cache_config import cache
from api.users_api import api_get
from api.study_api import get_study

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
cache.init_app(app)


#app.register_blueprint(api_get)
app.register_blueprint(get_study)

if __name__ == '__main__':
    app.run(debug=True)
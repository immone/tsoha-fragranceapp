from os import getenv
from flask import Flask

app = Flask(__name__, static_folder='static')
app.secret_key = getenv("SECRET_KEY")
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
app.config['UPLOAD_PATH'] = getenv("UPLOAD_PATH")

import entities.routes
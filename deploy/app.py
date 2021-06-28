
from flask import Flask

#Setting the folder to save de prediction image
UPLOAD_FOLDER = 'to_predict'

#Setting the basic deplosy
app = Flask(__name__)
app.secret_key = "pixforce"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
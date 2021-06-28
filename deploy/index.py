from flask import Flask, render_template, request, redirect, flash, url_for
import urllib.request
import base64
import numpy as np
from app import app
from prediction import get_prediction
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import os
from PIL import Image
import io

#Main route
@app.route('/')
def index():
    return render_template('index.html')

#Create a basic route for a sample index for api test
@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            label, acc = get_prediction(filename)
            flash(label)
            flash(acc)
            flash(filename)
            return redirect('/')

#Create a API resquest with JSON as output
@app.route('/predict', methods=['POST'])
def upload_file():
    response = {'success': False}
    if request.method == 'POST':

        if request.files.get('file'): 

            img_requested = request.files['file'].read()

            img = Image.open(io.BytesIO(img_requested))

            img = np.array(img) 

            label, acc = get_prediction(img)

            response['predictions'] = []

            row = {'label': label, 'confidence': float(acc)} 
            response['predictions'].append(row)

            response['success'] = True
            return jsonify(response)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run(threaded=False)
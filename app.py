# Developed by Camilo Correa Restrepo
# ccorre20@eafit.edu.co
# Version 2

# app.py
# This contains the main code for the web application, in particular,
# it allows the app to receive requests and respond to them.
from flask import Flask, request, redirect, flash
from werkzeug.utils import secure_filename
import os
from processing import classify

# This defines where images will be temporarily stored.
# While it is true that when run on a container this is done anyways when it is spun down,
# it is still a good idea to not clutter it with images.
UPLOAD_FOLDER = '/tmp'

# This initiates and configures the app.
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
# This is main method that controls the execution of the web app.
# It receives a file and hands it off to be processed.
# Otherwise it flashes an error.
def hello_world():
    print('request received')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # If the file is ok, save it to disk, and send it to the classification method.
        # It returns an html doc that is then rendered with the answer.
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return classify(filename)
    # If the request method was get, it will simply return a simple web page as a string.
    return '''
        <!doctype html>
        <head>
            <title>Location Recognition System</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Please upload a new File</h1>
            <p>Select an image and later click "upload" to launch classify it</p>
            <form method=post enctype=multipart/form-data>
              <p><input type=file name=file>
                 <input type=submit value=Upload>
            </form>
        </body>
        '''

if __name__ == '__main__':
    app.run()

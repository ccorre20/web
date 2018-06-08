# Developed by Camilo Correa Restrepo
# ccorre20@eafit.edu.co
# Version 2

# processing.py
# This contains the auxiliary code for the web application, in particular,
# it allows the app to classify images, and render their results as an html doc string.

import cv2 as cv2
import joblib
import os
import contextlib
import pandas as pd
import numpy as np

img_folder = '/tmp'

locations = {0: '18', 1: '19', 2: '26', 3: '38', 4: 'admisiones', 5: 'agora', 6: 'auditorio',
             7: 'biblioteca', 8: 'dogger', 9: 'idiomas'}

# Sets the number of clusters used by the model.
k = 500


# This helper method transforms a string into an html doc string with the answer inserted.
def response(ans):
    string = '''
        <!doctype html>
        <head>
            <title>Location Recognition System</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>The location was identified as</h1>
            <p>''' + ans + '''</p>
            <form method="get" action="/">
                <input type="submit" value="Return" name="Return"/>
            </form>
        </body>
        '''
    return string


# This is the most important method, it quickly loads both models, and calculates to what location each
# image corresponds.
def classify(filename):
    # This extracts the image
    img = cv2.cvtColor(cv2.imread(os.path.join(img_folder, filename)), cv2.COLOR_BGR2GRAY)

    # This will check the image size, and compress it if necessary to speed up execution.
    shape = img.shape
    if shape[0] > 2000:
        img = cv2.resize(img, (1280, 720))

    # This will extract the SIFT features of the image, and pass them into a dataframe.
    sift = cv2.xfeatures2d.SIFT_create()
    _, des = sift.detectAndCompute(img, None)
    df = pd.DataFrame(des)

    # Load the clustering model
    k_model = joblib.load('new_KMeans_'+str(k)+'.pkl')

    # Label all of the image's descriptors and constructs a histogram from the labeled descriptors.
    labels = k_model.predict(df.values)
    hist, _ = np.histogram(labels, k, density=True)

    # Load the classification model and classify the image
    clf = joblib.load('new_LinearSVC_'+str(k)+'.pkl')
    ans = locations[int(clf.predict([hist])[0])]

    # Remove the temporarily stored file
    with contextlib.suppress(FileNotFoundError):
        os.remove(os.path.join(img_folder, filename))

    # Return a formatted response using the helper method.
    return response(ans)

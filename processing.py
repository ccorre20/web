import cv2 as cv2
import joblib
import os
import contextlib
import pandas as pd
import numpy as np

img_folder = '/tmp'

locations = {0: '18', 1: '19', 2: '26', 3: '38', 4: 'admisiones', 5: 'agora', 6: 'auditorio',
             7: 'biblioteca', 8: 'idiomas', 9: 'dogger'}

k = 500

def classify(filename):
    img = cv2.cvtColor(cv2.imread(os.path.join(img_folder, filename)), cv2.COLOR_BGR2GRAY)

    h, w, c = img.shape

    if w > 2000:
        img = cv2.resize(img, (1280, 720))

    sift = cv2.xfeatures2d.SIFT_create()
    _, des = sift.detectAndCompute(img, None)

    df = pd.DataFrame(des)

    k_model = joblib.load('new_KMeans.pkl')

    labels = k_model.predict(df.values)

    hist, _ = np.histogram(labels, k, density=True)

    clf = joblib.load('new_LinearSVC.pkl')

    ans = locations[clf.predict([hist])]

    with contextlib.suppress(FileNotFoundError):
        os.remove(os.path.join(img_folder, filename))

    return ans

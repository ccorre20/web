import cv2 as cv2
import joblib
import os
import contextlib

img_folder = '/tmp'

locations = {0: '18', 1: '19', 2: '26', 3: '38', 4: 'admisiones', 5: 'agora', 6: 'auditorio',
             7: 'biblioteca', 8: 'idiomas', 9: 'dogger'}

def classify(filename):
    img = cv2.cvtColor(cv2.imread(os.path.join(img_folder, filename)), cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    _, des = sift.detectAndCompute(img, None)

    k_model = joblib.load('model_500.pkl')

    labels = k_model.predict(des)

    hist = {}

    for i in range(500):
        hist[i] = 0

    for l in labels:
        hist[l] = hist[l] + 1

    sample = list(hist.values())

    clf = joblib.load('LinearSVC_500.pkl')

    ans = locations[clf.predict([sample])[0]]

    with contextlib.suppress(FileNotFoundError):
        os.remove(os.path.join(img_folder, filename))

    return ans

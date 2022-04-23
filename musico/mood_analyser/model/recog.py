from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np
from django.conf import settings
import os

BASE_DIR = settings.BASE_DIR

face_classifier = cv2.CascadeClassifier(os.path.join(
    BASE_DIR, "mood_analyser", 'model/haarcascade_frontalface_default.xml'))
classifier = load_model(os.path.join(
    BASE_DIR, "mood_analyser", 'model/Emotion_little_vgg.h5'))

class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']

def return_mood(image_path):

    # cap = cv2.VideoCapture(image_path)
    cap = cv2.imread(image_path)

    try:
        gray = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        print(gray)
    except Exception as e:
        print("Error", e)
        return "No face detected"
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(cap, (x, y), (x+w, y+h), (238, 130, 238), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48),
                                interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = list(classifier.predict(roi)[0])

            # array to be sent to the frontend
            return preds.index(max(preds))
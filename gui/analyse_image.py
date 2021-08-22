import os
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import numpy as np
import tensorflow
from tensorflow import keras
from keras.applications.vgg16 import VGG16
from keras.utils.data_utils import get_file
import json
from matplotlib import pyplot as plt
import cv2 as cv


class analyse_image:
    def __init__(self):
        self.CLASS_INDEX = None
        self.CLASS_INDEX_PATH = "https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json"
        self.car_or_not_model = None
        self.damaged_or_not_model = None
        self.damage_location_model = None
        self.damage_severity_model = None

    def map(self, OldValue, OldMin, OldMax, NewMin, NewMax):
        OldRange = (OldMax - OldMin)  
        NewRange = (NewMax - NewMin)  
        NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
        return NewValue

    def get_prediction_damaged(self, model, path):
        img = cv.imread(path)
        img = cv.resize(img, (300,300))
        img = img.reshape(1, 300,300, 3)
        proba = model.predict(img)
        return (proba > 0.5).astype('int32')

    def damaged_or_not(self, path):
        if self.damaged_or_not_model == None:
            self.damaged_or_not_model = keras.models.load_model('C:/Users/serka/Desktop/gui/model_v2.h5')
        return self.get_prediction_damaged(self.damaged_or_not_model, path)
        
    def damage_location(self, path):
        damages = [' Kaporta ', ' Lastik ve/veya Tekerlek ', ' Cam ', ' Kapı ', ' Tampon ']
        if self.damage_location_model == None:
            self.damage_location_model = keras.models.load_model('C:/Users/serka/Desktop/gui/model_5/modelc5.h5')
        img = cv.imread(path)
        img = cv.resize(img, (300, 300))
        img = img.reshape(1, 300, 300, 3)
        prediction = self.damage_location_model.predict(img)
        return damages[np.argmax(prediction)]
        
    def damage_severity(self, path, anomaly_factor):
        damage_severities = [[0.0, 33.3], [33.3, 66.6], [66.6, 100.0]]
        if self.damage_severity_model == None:
            self.damage_severity_model = keras.models.load_model('C:/Users/serka/Desktop/gui/model_v3.h5')
        x = self.map(anomaly_factor, -50, 50, 0.5, 1.5)
        img = cv.imread(path)
        img = cv.resize(img, (300, 300))
        img = img.reshape(1, 300, 300, 3)
        pred = self.damage_severity_model.predict(img)
        
        damage = damage_severities[np.argmax(pred)]
        p = ((damage[0] + damage[1]) / 2) * x
        p = round(p, 3)
        if p > 100:
            return'100'
        else:
            return str(p)
    def get_predictions(self, predictions, top = 5):
        if self.CLASS_INDEX == None:
            fpath = get_file("imagenet_class_index.json",
                        self.CLASS_INDEX_PATH,
                        cache_subdir = "models")
            self.CLASS_INDEX = json.load(open(fpath))
        results = []
        for pred in predictions:
            top_indices = pred.argsort()[-top:][::-1]
            result = [tuple(self.CLASS_INDEX[str(i)]) + (pred[i],) for i in top_indices]
            result.sort(key=lambda x: x[2], reverse=True)
            results.append(result)
        return results

    def load_im(self, path):
        img = keras.preprocessing.image.load_img(path, target_size = (224, 224))
        img = img_to_array(img)
        img = np.expand_dims(img, axis = 0)
        img = preprocess_input(img)
        return img

    def car_or_not(self, filepath):
        if self.car_or_not_model == None:
            self.car_or_not_model = VGG16(weights = "imagenet")
        cat_list = np.load("C:/Users/serka/Desktop/gui/categories.npy")
        image = self.load_im(filepath)
        preds = self.get_predictions(self.car_or_not_model.predict(image))
        for j in preds[0]:
            if j[0:2] in cat_list:
                return 1
        return 0
import boto3
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np
import cv2
from keras.applications.mobilenet import MobileNet
from keras.models import model_from_json
from keras import backend as K
import os
import logging

SKIN_CLASSES = {
  0: 'Actinic Keratoses (Solar Keratoses) or intraepithelial Carcinoma (Bowen’s disease)',
  1: 'Basal Cell Carcinoma',
  2: 'Benign Keratosis',
  3: 'Dermatofibroma',
  4: 'Melanoma',
  5: 'Melanocytic Nevi',
  6: 'Vascular skin lesion'
}

s3_access_key = 'your_access_key_here'
s3_secret_key = 'your_secret_key_here'
s3_region = 'your_region_here'

s3_client = boto3.client('s3', aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key, region_name=s3_region)

s3_bucket_name = 'your_bucket_name_here'
s3_file_name = 'your_file_name_here'

def prepare_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = np.expand_dims(img, axis=0)
    img = img / 255.0
    return img

def disease_prediction(bucket_name, file_name):
    response = s3_client.get_object(Bucket=bucket_name, Key=file_name)

    # Read the image data from the response object
    image_data = response['Body'].read()

    # Do whatever you want with the image data here, such as saving it to a file
    with open('image.jpg', 'wb') as f:
        f.write(image_data)

    json_file = open('modelnew.json', 'r')
    loaded_json_model = json_file.read()
    json_file.close()
    model = model_from_json(loaded_json_model)
    model.load_weights('modelnew.h5')

    # Prepare image
    logging.info("reshaping Image")
    img = cv2.imread('image.jpg')
    img = prepare_image(img)

    # Make prediction
    logging.info("Predicting Image")
    prediction = model.predict(img)
    pred = np.argmax(prediction)
    disease = SKIN_CLASSES[pred]
    accuracy = prediction[0][pred]
    K.clear_session()

    final_dict = {"title": "Success", "predictions": disease, "acc": accuracy*100}

    return final_dict

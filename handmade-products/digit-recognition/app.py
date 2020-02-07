from flask import Flask, escape, request, render_template, jsonify
from keras.models import load_model
import os
import cv2
import numpy as np

import process_image as image_processor

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = Flask(__name__)

model = load_model('model.h5')
model._make_predict_function()

@app.route('/')
def main():
    return render_template('index.html')


def hello():
    name = request.args.get("name", "World")

    return f'Hello, {escape(name)}!'


@app.route('/process-image', methods=['POST'])
def process_image():
    image = request.files.get('image')
    image = cv2.imdecode(np.fromfile(image), cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    gray_image = 255 - cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray_image = image_processor.convert_image_for_mnist(gray_image)
    print(gray_image.reshape(1, 28, 28, 1).shape)

    prediction = model.predict(gray_image.reshape(1, 28, 28, 1))[0]

    for i in range(len(prediction)):
        num = prediction[i]

        if num > 0.8:
            return jsonify({'result': i})

    return jsonify({'result': -1})

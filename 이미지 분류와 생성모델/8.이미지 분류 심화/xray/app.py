from flask import Flask, render_template, request
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import os

app = Flask(__name__)

model = load_model("diagnose_pneumonia_model.keras")

IMAGE_SIZE = 150

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']

    if file:
        filepath = os.path.join("static", file.filename)
        file.save(filepath)

        img = cv2.imread(filepath)
        img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))
        img = img / 255.0
        img = np.reshape(img, (1, IMAGE_SIZE, IMAGE_SIZE, 3))

        prediction = model.predict(img)[0][0]

        if prediction > 0.5:
            result = "PNEUMONIA"
            prob = prediction
        else:
            result = "NORMAL"
            prob = 1 - prediction

        return render_template("result.html",
                               filename=file.filename,
                               result=result,
                               probability=round(float(prob), 4))

if __name__ == '__main__':
    app.run(debug=True)





from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)

model = tf.keras.models.load_model('c:/data/catdog/catdog_model.keras')

UPLOAD_DIR = 'static'
IMG_SIZE = (128,128)

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']

    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR, filename)  #디렉토리+파일이름 조립
    file.save(file_path)  #첨부파일이 static 디렉토리에 저장됨

    img = image.load_img(file_path, target_size=IMG_SIZE)
    img = image.img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)[0][0]

    result = 'Dog' if pred > 0.5 else 'Cat'

    return render_template(
        'result.html',
        result=result,
        image_path=file_path
    )


if __name__ == '__main__':
    app.run(debug=True)
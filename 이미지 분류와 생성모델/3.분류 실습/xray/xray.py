from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('input.html')

@app.route('/uploader', methods = ['POST'])
def upload_image():
    gender = request.form['gender']
    if gender == 'M':
        model = load_model('c:/data/models/xray_m_best.keras')
    elif gender == 'F':
        model = load_model('c:/data/models/xray_f_best.keras')

    img = Image.open(request.files['file'].stream)
    img = img.resize((80,100))
    arr = np.array(img) / 255
    arr = arr.reshape(1,80,100,3)
    pred = model.predict(arr)

    return '연령:' + str(pred[0][0])


if __name__ == '__main__':
    app.run(port=8000, threaded=False)
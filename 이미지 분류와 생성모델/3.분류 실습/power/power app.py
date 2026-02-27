from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from keras.models import load_model

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('input.html')


@app.route('/uploader', methods=['POST'])
def upload_image():
    model = load_model('c:/data/models/power_best.keras')
    img = Image.open(request.files['file'].stream)
    img = img.resize((32, 20))
    arr = np.array(img) / 255
    arr = arr.reshape(1, 32, 20, 3)
    pred = model.predict(arr)
    return '숫자:' + str(pred[0][0])


if __name__ == '__main__':
    app.run(port=8000, threaded=False)






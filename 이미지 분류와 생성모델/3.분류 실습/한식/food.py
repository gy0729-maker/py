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
    model = load_model('c:/data/models/food_best.keras')
    img = Image.open(request.files['file'].stream)
    img = img.resize((96,96))
    arr = np.array(img) / 255
    arr = arr.reshape(1,96,96,3)
    menu_items = ['치킨','돌솥비빔밥','제육볶음','김치','삼겹살','된장찌개']
    pred = model.predict(arr)
    num = np.argmax(pred, axis=1)
    return '메뉴:' + menu_items[num[0]]

if __name__ == '__main__':
    app.run(port=8000, threaded=False)
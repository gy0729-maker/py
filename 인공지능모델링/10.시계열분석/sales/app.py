from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

model = load_model('c:/data/test/sales_rnn_model.keras')

df = pd.read_csv('c:/data/test/sales_time.csv')
scaler = MinMaxScaler()
scaler.fit(df['sales'].values.reshape(-1,1))


@app.route('/')
def home():
    return render_template('input.html')

@app.route('/predict', methods = ['POST'])
def predict():
    values = request.form.get('values')
    nums = np.array([float(x) for x in values.split(',')]).reshape(-1,1)

    scaled = scaler.transform(nums)
    X = scaled.reshape(1,3,1)

    pred = model.predict(X)
    predicted_sales = scaler.inverse_transform(pred)[0][0]

    recent_avg = nums.mean()

    if predicted_sales < recent_avg * 0.95:
        action = '프로모션 또는 할인 추천'
    elif predicted_sales > recent_avg * 1.05:
        action = '재고 확보 및 인력 보강'
    else:
        action = '현 상태 유지'

    return render_template(
        'result.html',
        prediction = round(predicted_sales, 1),
        action = action
    )

if __name__ == '__main__':
    app.run(debug=True)

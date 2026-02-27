from flask import Flask, render_template, request
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np

model = joblib.load('c:/data/test/customer_sales.model')
scaler = joblib.load('c:/data/test/scaler.pkl')
app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return render_template('input.html')

@app.route('/result',methods=['POST'])
def predict():

    a = int(request.form['a'])
    b = int(request.form['b'])
    c = int(request.form['c'])
    test_set = np.array([[a, b, c]])
    test_set = scaler.transform(test_set)

    rate=model.predict_proba(test_set)
    if rate[0][1]>=0.5:
        result='높음'
    else:
        result='낮음'

    return render_template('result.html', rate='{:.2f}%'.format(rate[0][1]*100), result=result)



if __name__ == '__main__':
    app.run(debug=True)
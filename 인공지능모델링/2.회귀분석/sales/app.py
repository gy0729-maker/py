from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

model = joblib.load('ads_sales_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    tv = float(request.form.get('tv'))
    radio = float(request.form.get('radio'))
    sns = float(request.form.get('sns'))

    result = model.predict([[tv,radio,sns]])
    sales = result[0]

    return render_template('result.html', predicted_sales=sales, tv=tv, radio=radio, sns=sns)

if __name__ == '__main__':
    app.run(port=8000, threaded=False)

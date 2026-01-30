from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

bundle = joblib.load('c:/data/house/house_price.joblib')
model = bundle['model']
feature_names = bundle['feature_names']

@app.get('/')
def home():
    return render_template('index.html')

@app.post('/predict')
def predict():
    sqm = float(request.form.get('sqm',''))
    rooms = float(request.form.get('rooms',''))

    X = pd.DataFrame([[sqm,rooms]], columns=feature_names)
    pred_raw = float(model.predict(X)[0])
    print(pred_raw)
    pred = pred_raw / 100

    return render_template(
        'result.html',
        prediction=f'{pred:.2f}',
        sqm=sqm,
        rooms=int(rooms)
    )

if __name__ == '__main__':
    app.run(debug=True)
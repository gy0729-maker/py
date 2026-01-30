from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

model = joblib.load('cluster_model.pkl')
scaler = joblib.load('scaler.pkl')

cluster_desc = {
    0: '고소득 · 소비성향 낮음 (절약형 고객)',
    1: "저소득 · 소비성향 높음 (핵심 타겟 고객)",
    2: "중간소득 · 평균적 소비성향 (일반 고객)"
}

@app.route('/')
def home():
    return render_template('input.html')

@app.route('/predict',methods=['POST'])
def predict():
    age = int(request.form['age'])
    income = int(request.form['income'])
    score = int(request.form['spending_score'])

    X = np.array([[age,income,score]])
    X_scaled = scaler.transform(X)

    cluster = model.predict(X_scaled)[0]
    description = cluster_desc.get(cluster, '해석 불가')

    return render_template(
        'result.html',
        age = age,
        income = income,
        score = score,
        cluster = cluster,
        description = description
    )

if __name__ == '__main__':
    app.run(debug=True)
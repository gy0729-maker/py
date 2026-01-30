from flask import Flask, render_template, request
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

model = load_model('c:/data/test/student_model.keras')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods = ['POST'])
def predict():
    study_hours = float(request.form['study_hours'])
    attendance_rate = float(request.form['attendance_rate'])
    assignment_score = float(request.form['assignment_score'])

    X = np.array([[study_hours, attendance_rate, assignment_score]])

    pred = model.predict(X)

    return render_template(
        'result.html',
        study_hours = study_hours,
        attendance_rate = attendance_rate,
        assignment_score = assignment_score,
        result = pred[0][0]
    )

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
from statsmodels.regression.linear_model import OLSResults

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return render_template('ozone/input.html')

@app.route('/result',methods=['POST'])
def result():
    model = OLSResults.load('c:/data/ozone/ozone_regress.model')
    a = float(request.form['a'])
    b = float(request.form['b'])
    c = float(request.form['c'])
    test_set = [a,b,c]
    ozone = model.predict(test_set)
    return render_template('ozone/result.html',ozone='{:.2f}'.format(ozone[0]), a=a, b=b, c=c)

if __name__ == '__main__':
    app.run(port=8000, threaded=False)




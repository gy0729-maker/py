from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return render_template('rides/input.html')

@app.route('/result',methods=['POST'])
def result():
    model = joblib.load('c:/data/rides/rides_regression.model')
    a = int(request.form['a'])
    b = int(request.form['b'])
    c = int(request.form['c'])
    d = int(request.form['d'])
    e = int(request.form['e'])
    f = int(request.form['f'])
    g = int(request.form['g'])
    if g==0:
        h=1
    elif g==1:
        h=0

    test_set = [[a,b,c,d,e,f,g,h]]
    result = model.predict(test_set)
    return render_template('rides/result.html',
                           point='{:.2f}'.format(result[0]), a=a,b=b,c=c,d=d,e=e,f=f,g=g,h=h)
if __name__ == '__main__':
    app.run(port=8000, threaded=False)

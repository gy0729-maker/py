from flask import Flask, render_template, request
import torch

app = Flask(__name__)

checkpoint = torch.load(
    'c:/data/test/regression_model.pt',
    map_location='cpu',
    weights_only=False  #전체 객체 불러오기 허용(가중치만 불러오기X)
)

model = checkpoint['model']
model.eval()

scaler_X = checkpoint['scaler_X']
scaler_y = checkpoint['scaler_y']


@app.route('/')
def index():
    return render_template('input.html')

@app.route('/predict', methods=['POST'])
def predict(): #request:내장객체
    sq = float(request.form['SquareFeet'])
    br = float(request.form['Bedrooms'])
    age = float(request.form['Age'])

    X_input = scaler_X.transform([[sq, br, age]])
    X_tensor = torch.tensor(X_input, dtype=torch.float32)
    y_pred_scaled = model(X_tensor).detach().numpy()   #detach->순전파만(역전파 끄기)
    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1,1))[0][0]
                #역스케일링 .inverse_transform
    y_pred_formatted = '{:,.0f}'.format(y_pred)

    return render_template('result.html', prediction=y_pred_formatted)


if __name__ == '__main__':
    app.run(debug=True)
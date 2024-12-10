from flask import Flask, render_template, url_for, request # type: ignore
import pickle
import numpy as np # type: ignore
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

model = pickle.load(open('random_forest_regressor.pkl', 'rb'))

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['Post'])
def predict():
    Fuel_Type_Petrol, Fuel_Type_Diesel = 0, 0
    Seller_Type_Individual, Transmission_Manual = 0, 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Year = 2024 - Year
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        Fuel_Type = request.form['Fuel_Type']
        if Fuel_Type == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif Fuel_Type == 'Diesel':
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0
        Seller_Type = request.form['Seller_Type']
        if Seller_Type == 'Individual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_type = request.form['Transmission_Type']
        if Transmission_type == 'Manual':
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

        prediction = model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        output = round(prediction[0], 2)

        if output < 0:
            return render_template('index.html', Prediction_Text = 'Sorry, you cannot sell this car')
        else:
            return render_template('index.html', Prediction_Text = ' You can sell this car at {}'.format(output))
        


if __name__ == '__main__':
    app.run(debug=True)
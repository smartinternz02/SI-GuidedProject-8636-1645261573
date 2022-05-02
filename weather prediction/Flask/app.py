import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)#our flask app
model = pickle.load(open('weather_ml.pkl', 'rb')) #loading the model

@app.route('/')
def home():
    return render_template('home.html')#rendering html page

@app.route('/pred')
def index():
    return render_template('index.html')#rendering prediction page

@app.route('/predict',methods=['POST'])
def y_predict():
    if request.method == "POST":
        ds = request.form["Date"]
        #Converting date input to a dataframe
        a={"ds":[ds]}
        ds=pd.DataFrame(a)
        ds['year'] = pd.DatetimeIndex(ds['ds']).year
        ds['month'] = pd.DatetimeIndex(ds['ds']).month
        ds['day'] = pd.DatetimeIndex(ds['ds']).day
        ds.drop('ds', axis=1, inplace=True)
        ds=ds.values.tolist()
        #print(ds)
        #predicting the temperature for the user given input date
        prediction = model.predict(ds)
        #print(prediction[0])
        output=round(prediction[0],2)#rounding off the decimal values to 2
        print(output)
        return render_template('index.html',prediction_text="Temperature on selected date is. {} degree celsius".format(output))
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)

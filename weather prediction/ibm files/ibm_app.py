import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
#import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Y1PZtY26CqnT7buS4DHWpxhGwReOd29HZSvYiJ0y3jGp"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)#our flask app
#model = pickle.load(open('weather_prediction.pickle', 'rb')) #loading the model

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
        payload_scoring = {"input_data": [{"fields": [["year", "month","date"]], "values": ds}]}
        #payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/54f8f5b6-3db8-4031-a8ef-933867c71746/predictions?version=2022-03-05', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        pred= response_scoring.json()
        print(pred)
        output= pred['predictions'][0]['values'][0][0]
        print(output) 
        
        return render_template('index.html',prediction_text="Temperature on selected date is. {} degree celsius".format(output))
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=False)

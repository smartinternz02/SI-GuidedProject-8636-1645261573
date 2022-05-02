import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
#import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "M_JRaxyOhRdVQucqo4quoREqJIA8bZPLXf-0AI1Q8Lpa"
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

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/20c988c4-cf6d-48e6-85fe-3d5cef272632/predictions?version=2021-12-09', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        pred= response_scoring.json()
        print(pred)
        output= pred['predictions'][0]['values'][0][0]
        output=round(output,2)#rounding off the decimal values to 2
        #print(output)
        
        return render_template('index.html',prediction_text="Temperature on selected date is. {} degree celsius".format(output))
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=False)

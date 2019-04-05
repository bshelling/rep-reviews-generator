# Reputation.com Reviews Report Generator
# Author: Brandon Shelling
# Email: bshelling@gmail.com
#
# Active environment: source env/bin/activate
# Run Server: FLASK_APP=app.py flask run
import requests
import csv
import json
from flask import Flask, render_template, request, redirect
import os
import wget
app = Flask(__name__)


# Repuations Keys
API_KEY = os.getenv('API_KEY')
SURVEY_ID = os.getenv('SURVEY_ID')
URL = 'https://api.reputation.com/v3/reviews?limit='

#Authorization Header
headers = {
    'content-type':'application/json',
    'X-API-KEY': API_KEY
}



@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', files=os.listdir('./files')) 
    else:
        req = requests.get(URL + request.form['limit'],headers=headers)
        with open('files/'+ request.form['filename'] +'.csv', 'w', newline='') as dataFile:
            dataWrite = csv.writer(dataFile, delimiter=",")
            dataWrite.writerow(['id','tenantID','sourceID','url','date','reviewer','rating','normalizedRating','sentiment','commentTitle','comment','canRespond','hasResponses','responseUrl','reviewUrl','categories'])
            for review in req.json()['reviews']:
                dataWrite.writerow([ review['id'], review['tenantID'], review['locationID'], review['locationName'], review['sourceID'], review['url'], review['date'], review['reviewer'], review['rating'], review['normalizedRating'], review['sentiment'], review['commentTitle'], review['comment'], review['canRespond'], review['hasResponses'], review['responseUrl'], review['reviewUrl'], review['categories']])
        return redirect('/')


@app.route('/delete')
def deleteFiles():
    files = os.listdir('./files');
    for file in files:
        os.remove('./files/'+file)
    return redirect('/')

      



    




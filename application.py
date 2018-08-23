from flask import Flask, request, render_template, Response, jsonify
from flask_bootstrap import Bootstrap
from Modules.preprocess_helper import *
import json
import numpy as np
import pandas as pd
import pickle
from wtforms import TextField, Form

application = Flask(__name__)
bootstrap = Bootstrap(application)

with open("random_forest_model.pkl", "rb") as file:
    model = pickle.load(file)
with open('df_5w.pkl', 'rb') as file:
    df_5w = pickle.load(file)
with open ('names.pkl', 'rb') as file:
    fighters = pickle.load(file)

@application.route('/autocomplete1', methods=['GET'])
@application.route('/autocomplete2', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    res = [x for x in fighters if search.lower() in x.lower()]
    return jsonify(matching_results=res)

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@application.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        result = request.form

        fighter1 = result['fighter1'].split(' ')
        fighter2 = result['fighter2'].split(' ')
        stat1 = df_5w[(df_5w['first'].str.lower() == fighter1[0].lower()) &
                (df_5w['last'].str.lower() == fighter1[1].lower())]
        stat2 = df_5w[(df_5w['first'].str.lower() == fighter2[0].lower()) &
                (df_5w['last'].str.lower() == fighter2[1].lower())]
        stat1.loc[:,'result'] = 'n/a'
        stat2.loc[:,'result'] = 'n/a'

        delta = generate_delta(stat1, stat2).iloc[:,:-1].values
        prediction = model.predict(delta)

        return render_template('result.html', prediction=prediction)

if __name__ == "__main__":
    application.debug = True
    application.run()
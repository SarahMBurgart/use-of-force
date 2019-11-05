from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
import dill as pickle
from urllib.request import urlopen
from urllib.parse import quote
import json
from findbeat import findbeat
from pandas.io.formats.style import Styler


app = Flask(__name__)



def get_model():
     # add unpickled model
    with open('lrbimod.pkl', 'rb') as modelZ:
        model = pickle.load(modelZ)
    with open('gbc1234.pkl', 'rb') as modelW:
        model1234 = pickle.load(modelW)
    with open ('logr_cols', 'rb') as lc:
        logr_cols= pickle.load(lc)
    with open ('col_lst', 'rb') as fp:
        col_lst= pickle.load(fp)
    with open('sgr_df.pkl', 'rb') as sgr:
        sgr_df = pickle.load(sgr)
    with open('coo', 'rb') as c:
        coo = pickle.load(c)
        
    #print("hi")
    return model, model1234, logr_cols, col_lst, sgr_df, coo


model, model1234, logr_cols, col_lst, sgr_df, coo = get_model()

@app.route('/table', methods = ['GET'])
def table():
    return coo.style.render(index=False)

@app.route('/', methods=['GET'])
def home():
    return render_template('login.html')

@app.route('/visualizations', methods=['GET'])
def visualizations():
    return render_template('visualizations.html')

@app.route('/predictions', methods=['GET'])
def predictions():
    return render_template('predictions.html')

@app.route('/solve', methods=['POST'])
def solve():
    
    user_data = request.json
    #print(user_data)
    address, ICT, race, gender, hour, dayofweek, month = user_data["Address"], user_data["ICT"], user_data["Race"], user_data["Gender"], user_data["Hour"], user_data["dayofweek"], user_data["month"]
    p = _probas(address, ICT, race, gender, hour, dayofweek, month)
    
    return jsonify({'p0':p[0], 'p1':p[1],'p2':p[2],'p3':p[3],'p4':p[4]})




def _probas(address, ICT, race, gender,  hour, dayofweek, month):
    precinct, sector, beat = _get_beat(address)
    coshour, sinhour = _get_hours(hour)
    
    
    d = pd.DataFrame(np.zeros((1,161), dtype=np.float64), columns=logr_cols)
    d.loc[0,f"P_{precinct}"] = 1
    d.loc[0,f"S_{sector}"] = 1
    d.loc[0,f"B_{beat}"] = 1

    d.loc[0,f"ICT_{ICT}"] = 1
    d.loc[0,f"dow_{dayofweek}"] = 1
    d.loc[0,'CT_911'] = 1
    d.loc[0,f"month_{month}"] = 1
    d.loc[0, "sin_hour2"] = sinhour
    d.loc[0, "cos_hour2"] = coshour

    pp_1 = model.predict_proba(d)

    
    d2 = pd.concat([d, sgr_df], axis=1, sort=False)
    d2.loc[0,f"SG_{gender}"] = 1
    d2.loc[0,f"SR_{race}"] = 1

    pp_2 = model1234.predict_proba(d2)
    print(pp_1, pp_2)
    p_list = []

    p_list.append(pp_1[0][0])
    p_list.append(pp_1[0][1]*pp_2[0][0])
    p_list.append(pp_1[0][1]*pp_2[0][1])
    p_list.append(pp_1[0][1]*pp_2[0][2])
    p_list.append(pp_1[0][1]*pp_2[0][3])

    print(pp_1, pp_2, p_list)
    return p_list

def _get_beat(address):
    beat = findbeat(address)
    precinct = _get_precinct(beat)

    with open('sectors_lst', 'rb') as pl:
        sectors = pickle.load(pl)
    
    result = [i for i in sectors if i.startswith(beat[:1])]
    sector = result[0]
    return precinct, sector, beat

def _get_precinct(beat):
    if beat[0] in ["C", "E", "G"]:
        precinct = "EAST"
    elif beat.startswith("Q" or "M" or "D" or "K"):
        precinct = "WEST"
    elif beat.startswith("C" or "E" or "G"):
        precinct = "EAST"
    elif beat.startswith("S" or "R" or "O"):
        precinct = "SOUTH"
    elif beat.startswith("W" or "F"):
        precinct = "SOUTHWEST"
    else:
        precinct = "SOUTH"
    
    
    return precinct  


def _get_hours(hour):
    hour = int(hour)
    hour2 = (hour/24)*2*np.pi
    sinhour = np.sin(hour2)
    coshour = np.cos(hour2)

    return coshour, sinhour

    



if __name__ == '__main__':

    

    app.run(host='0.0.0.0', port=80)

    # (base) Sarahs-MacBook-Air-2:website sarahburgart$ export FLASK_ENV=development
 # (base) Sarahs-MacBook-Air-2:website sarahburgart$ flask run

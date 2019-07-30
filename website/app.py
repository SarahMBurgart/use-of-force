from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
import dill as pickle
from urllib.request import urlopen
from urllib.parse import quote
import json
from findbeat import findbeat

app = Flask(__name__)



def get_model():
     # add unpickled model
    with open('logr_model.pkl', 'rb') as modelZ:
        model = pickle.load(modelZ)
    with open ('col_lst', 'rb') as fp:
        col_lst= pickle.load(fp)
        
    #print("hi")
    return model, col_lst


model, col_lst = get_model()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

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
    address, ICT, race, gender, dayofweek, month, hour = user_data["Address"], user_data["ICT"], user_data["Race"], user_data["Gender"], user_data["dayofweek"], user_data["month"], user_data["hour"]
    p = _probas(address, ICT, race, gender, dayofweek, month, hour)
    
    return jsonify({'p0':p[0], 'p1':p[1],'p2':p[2],'p3':p[3],'p4':p[4]})




def _probas(address, ICT, race, gender, dayofweek, month, hour):
    precinct, sector, beat = _get_beat(address)
    coshour, sinhour = _get_hours(hour)
    
    
    d = pd.DataFrame(np.zeros((1,169), dtype=np.float64), columns=col_lst)
    d.loc[0,f"P_{precinct}"] = 1
    d.loc[0,f"S_{sector}"] = 1
    d.loc[0,f"B_{beat}"] = 1
    d.loc[0,f"SG_{gender}"] = 1
    d.loc[0,f"SR_{race}"] = 1
    d.loc[0,f"ICT_{ICT}"] = 1
    d.loc[0,f"dow_{dayofweek}"] = 1
    d.loc[0,'CT_911'] = 1
    d.loc[0,f"month_{month}"] = 1
    d.loc[0, "sin_hour2"] = sinhour
    d.loc[0, "cos_hour2"] = coshour
    #print(f"this is d:{d[["precinct"]]}")
    print(d.loc[0, "SG_Female"])
    #print(type(d.loc[0,"SG_Female"]), d["sin_hour2"], type(d.loc[0,"sin_hour2"]))
    p = model.predict_proba(d)
    print(p)
    return p[0]

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
    hour2 = (hour/24)*2*np.pi
    sinhour = np.sin(hour2)
    coshour = np.cos(hour2)

    return coshour, sinhour

    



if __name__ == '__main__':

    

    app.run(host='0.0.0.0', port=8087, debug=True)

    # (base) Sarahs-MacBook-Air-2:website sarahburgart$ export FLASK_ENV=development
 # (base) Sarahs-MacBook-Air-2:website sarahburgart$ flask run
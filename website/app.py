from flask import Flask, request, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predictions', methods=['POST'])
def predictions():
    user_data = request.json
    address, ICT, race, gender = user_data["Address"], user_data["ICT"], user_data["Race"], user_data["Gender"]
    p0,p1,p2,p3,p4 = _probas(address, ICT, race, gender)
    return jsonify({'p0':p0, 'p1':p1,'p2':p2,'p3':p3,'p4':p4})

def _probas(address, ICT, race, gender, fit_model):
    precinct, sector, beat = get_beat(address)
    month, dayofweek, coshour, sinhour = get_datetime()
    X = pd.DataFrame({"Precinct": precinct, "Sector": sector, "Beat": beat, "cat_ICT": ICT, "SubjectRace": race, "SubjectGender": gender, "coshour2": coshour, "sinhour2": sinhour, "month": month, "dayofweek": dayofweek})
    p = fit_model.predict_proba(X)


    return p[0], p[1], p[2], p[3], p[4]

def _get_beat(address):

    return precinct, sector, beat

def _get_datetime():

    return month, dayofweek, coshour, sinhour

    #return render_template('predictions.html')

@app.route('/visualizations', methods=['GET'])
def visualizations():
    return render_template('visualizations.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8087, debug=True)
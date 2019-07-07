import pandas as pd
import numpy as np
from datetime import datetime

class New_Call:
    def __init__(gender, race, reason, beat):
    now = datetime.datetime.now()
    self.month = now.month
    self.day = now.day
    self.hour = now.hour
    self.day_of_week = now.dt.dayofweek
    self.beat = beat
    self.gender = gender
    self.race = race
    self.reason = reason
    self.df = pd.DataFrame(columns=["force_beat", "Subject_Gender", "Subject_Race", "Initial_Call_Type", "month", "day", "day_of_week", "call_hour"])
    self.df.loc[0] = [self.beat, self.gender, self.race, self.reason, self.month, self.day, self.day_of_week, self.hour]

    # race, reason both need to be drop down menus


    def __predict__(self):

        self.df = pd.get_dummies(data = self.df, 
                        columns=["force_beat", 
                                "Subject_Gender", "Subject_Race", "Initial_Call_Type"], 
                        prefix=["forceb",  
                                "Gender",  "Race", "InitCall"])
    

    return self.df
# code to clean up calls.csv and move it to a SQL table
import sqlite3
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)
import numpy as np
import pandas as pd

calls = pd.read_csv("data/Call_Data.csv")

def callstime(df, col_arrive):
    yearmonthday = df[col_arrive].astype(str).str.split()
    df["year"] = yearmonthday.apply(lambda x: x[2])
    df["day"] = yearmonthday.apply(lambda x: x[1])
    month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec":12}
    df["month"] = yearmonthday.apply(lambda x: month_dict[x[0]])
    df["time"] = yearmonthday.apply(lambda x: x[3])
    return df

calls = callstime(calls,"Arrived Time")
calls17 = calls[calls["year"].isin(["2014", "2015", "2016", "2017", "2018", "2019"])]

# calculate and add column for epoch time
bar = pd.to_datetime( calls17["Arrived Time"], format="%b %d %Y %I:%M:%S:%f%p" )
epoch_second2 = bar.map(lambda x: x.value/1e9)
calls17["epoch_calls"] = epoch_second2

rs = calls17["CAD Event Number"].value_counts()
two = []
for v, i in zip(rs.values, rs.index):
    if v >1:
        two.append(i)
# len(two) == 362  
st = [x > 1 for x in rs]
dt =rs[st]

t = calls17[calls17["CAD Event Number"].isin(two)]
indt = t[t["Event Clearance Description"] == "-"].index
indt

calls17.drop(indt, axis=0, inplace=True)

#remove repetitive columns
calls_tosql = calls17.drop(columns =["day", "month", "time", "Precinct", "Sector", "Arrived Time"])
calls_tosql.set_index("epoch_calls", inplace=True)

# move calls to sqlite table - DONT REPEAT
calls_tosql.to_sql("log", con=cnx, index=True, if_exists="replace")

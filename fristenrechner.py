from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
from pandas.tseries.offsets import MonthEnd

import flask
from flask import request
"""
message = [
    {"conversationId": "1",
    "type": "webhook",
    "name": "message_sent",
    "messages": [
      {"type": "message",
       "data":
           {"type": "text/plain",
            "content": "30.09.2021"
           }
       }]
     }
]


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%d.%m.%Y")
    d2 = datetime.strptime(d2, "%d.%m.%Y")
    print(abs((d2 - d1).days))


days_between('30.09.2021', '01.07.2021')

"""
#Ausgabe Tag des Kündigungstags bei Angabe Kündigungstermin (Tag des Auszugs)
#Eingabe: Tag des Auszugs (Kündigungstermin)
def noticePeriod(date):
    sundays = 0
    days = [1,2,3]
    date = datetime.strptime(date, "%d.%m.%Y") + relativedelta(months=-3)
    for n in days:
        wd = timedelta(days=n)
        latest_notice_date = date + wd
        wdCheck = latest_notice_date.weekday()
        if wdCheck == 6:
            sundays = sundays + 1
    if sundays > 0:
        latest_notice_date = date + timedelta(days=4)
        print(latest_notice_date)
        return(latest_notice_date)
    else:
        latest_notice_date = date + timedelta(days=3)
        print(latest_notice_date)
        return(latest_notice_date)

#noticePeriod('31.01.2021')


#Ausgabe Tag des Auszugs (Kündigungstermin) bei Angabe Kündigungstag
def dayMoveOut(date):
    sundays = 0
    days = [0,1,2]
    date = datetime.strptime(date, "%d.%m.%Y")
    fom = date.replace(day=1)
    for n in days:
        wd = timedelta(days=n)
        bd = fom + wd
        wdCheck = bd.weekday()
        if wdCheck == 6:
            sundays = sundays + 1
    if sundays > 0:
        fbdom = fom + timedelta(days=3)
    else:
        fbdom = fom + timedelta(days=2)
    if fbdom >= date:
        date = date + relativedelta(months=+2)
        dmo = pd.to_datetime(date, format='%Y-%m-%d') + MonthEnd(1)
        print(dmo)
        return dmo
    else:
        date = date + relativedelta(months=+3)
        dmo = pd.to_datetime(date, format='%Y-%m-%d') + MonthEnd(1)
        print(dmo)
        return dmo

#dayMoveOut('05.08.2021') 

"""
def extractDate(userMessage):
    if(len(userMessage) == 0):
        date = ""
    else:
        date = userMessage['messages'][0]['data']['content']
    return date


#App
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route("/0.0.0.0", methods=["GET"])
def defaultFunction():
    return ""<h1>Fristenrechner</p>"" ###einmal anführungsstriche ergänzen


@app.route("/", methods=["GET"])  # localhost
def home():
    return ""<h1>Fristenrechner</p>"" ###einmal anführungsstriche ergänzen


@app.route("/noticePeriod", methods=["POST"])
def api_response_message():
    message =  request.get_json(force=True)
    date = extractDate(message)
    if(len(date) == 0):
        return "No date was detected!"    
    notice = noticePeriod(date)
    return (notice)


if __name__ == '__main__':
    app.run(debug=True)
"""
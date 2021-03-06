from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
from pandas.tseries.offsets import MonthEnd
import logging
import json
import requests

import flask
from flask import request

logging.basicConfig( level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

def checkDateFormat(date):
    try:
        if date != datetime.strptime(date, '%d.%m.%Y').strftime('%d.%m.%Y'):
            raise ValueError
        return True
    except ValueError:
        return False

#3-Monatsfrist
#Ausgabe Tag des Kündigungstags bei Eingabe Kündigungstermin
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
        latest_notice_date = datetime.strftime(latest_notice_date, "%d.%m.%Y")
        output = "Ihr Kündigungstag ist der "+latest_notice_date+"."
        print(output)
        return(output)
    else:
        latest_notice_date = date + timedelta(days=3)
        latest_notice_date = datetime.strftime(latest_notice_date, "%d.%m.%Y")
        output = "Ihr Kündigungstag ist der "+latest_notice_date+"."
        print(output)
        return(output)


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
        dmo = datetime.strftime(dmo, "%d.%m.%Y")
        output = "Ihr frühstmöglicher Kündigungstermin ist der "+dmo+"."
        print(output)
        return output
    else:
        date = date + relativedelta(months=+3)
        dmo = pd.to_datetime(date, format='%Y-%m-%d') + MonthEnd(1)
        dmo = datetime.strftime(dmo, "%d.%m.%Y")
        output = "Ihr Kündigungstermin ist der "+dmo+"."
        print(output)
        return output

#Ausgabe Tag des schnellstmöglichen Kündigungstermins
def dayMoveOutFast():
    sundays = 0
    days = [0,1,2]
    date = datetime.now()
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
        dmo = datetime.strftime(dmo, "%d.%m.%Y")
        output = "Ihr schnellstmöglicher Kündigungstermin ist der "+dmo+"."
        print(output)
        return output
    else:
        date = date + relativedelta(months=+3)
        dmo = pd.to_datetime(date, format='%Y-%m-%d') + MonthEnd(1)
        dmo = datetime.strftime(dmo, "%d.%m.%Y")
        output = "Ihr schnellstmöglicher Kündigungstermin ist der "+dmo+"."
        print(output)
        return output
    
#14-Tagefrist (Sonderregelung 549 II Nr. 2 BGB: Kündigung spätestens am 15. eines Monats zum Ablauf des Monats)
#Ausgabe Tag des Kündigungstags bei Eingabe Kündigungstermin
#Eingabe: Tag des Auszugs (Kündigungstermin)
def noticePeriodSonder(date):
    
    date = datetime.strptime(date, "%d.%m.%Y")
    month = str(date.month)
    print(month)
    year = str(date.year)
    print(year)
    output = "Ihr spätester Kündigungstag ist der 15."+month+"."+year+"."
    print(output)
    return(output)

#Ausgabe Tag des Auszugs (Kündigungstermin) bei Eingabe Kündigungstag
#Eingabe: Kündigungstag
def dayMoveOutSonder(date):

    date = datetime.strptime(date, "%d.%m.%Y")
    day = date.day

    if day <= 15:
        dmo = pd.to_datetime(date, format='%Y-%m-%d') + MonthEnd(1)
        dmo = datetime.strftime(dmo, "%d.%m.%Y")
        output = "Ihr Kündigungstermin ist der "+dmo+"."
        print(output)
        return(output)

    else:
        dmo = pd.to_datetime(date, format='%Y-%m-%d') + MonthEnd(2)
        dmo = datetime.strftime(dmo, "%d.%m.%Y")
        output = "Ihr Kündigungstermin ist der "+dmo+"."
        print(output)
        return(output)

#Ausgabe Tag des schnellstmöglichen Auszugs (Kündigungstermin) bei Eingabe aktuelles Datum
#Eingabe: -; Wird aus aktuellem Datum bestimmt
def dayMoveOutSonderFast():

    date = datetime.now()
    day = date.day

    if day <= 15:
        dmo = pd.to_datetime(date, format='%Y-%m-%d') + MonthEnd(1)
        dmo = datetime.strftime(dmo, "%d.%m.%Y")
        output = "Ihr schnellstmöglicher Kündigungstermin ist der "+dmo+"."
        print(output)
        return(output)

    else:
        dmo = pd.to_datetime(date, format='%Y-%m-%d') + MonthEnd(2)
        dmo = datetime.strftime(dmo, "%d.%m.%Y")
        output = "Ihr schnellstmöglicher Kündigungstermin ist der "+dmo+"."
        print(output)
        return(output)
    
    
#Datum extrahieren
def extractDate1(userMessage):
    if(len(userMessage) == 0):
        intent = ""
    else:
        intent = userMessage['messages'][0]['metaData']['slotFillingParameter']['kündigungstermin']
    return intent

def extractDate2(userMessage):
    if(len(userMessage) == 0):
        intent = ""
    else:
        intent = userMessage['messages'][0]['metaData']['slotFillingParameter']['kündigungstag']
    return intent

def extractDate3(userMessage):
    if(len(userMessage) == 0):
        intent = ""
    else:
        intent = userMessage['messages'][0]['metaData']['slotFillingParameter']['kündigungstag_sonder']
    return intent

def extractDate4(userMessage):
    if(len(userMessage) == 0):
        intent = ""
    else:
        intent = userMessage['messages'][0]['metaData']['slotFillingParameter']['kündigungstermin_sonder']
    return intent

def extractConversationId(userMessage):
    if(len(userMessage) == 0):
        conversationId = ""
    else:
        conversationId = userMessage['conversationId']
    return conversationId    

def createAnswer(conversationId, DateTime):
    payload = {
      "conversationId" : conversationId,
      "messages": [
        {
          "type" : "message",
          "data" : {
            "type" : "text/plain",
            "content" : DateTime
          }
        }
      ]
    }
    return json.dumps(payload)


#App
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route("/0.0.0.0", methods=["GET"])
def defaultFunction():
    return """<h1>Fristenrechner</h1>""" 


@app.route("/", methods=["GET"])  # localhost
def home():
    return """<h1>Fristenrechner</h1>""" 


@app.route("/noticePeriod", methods=["POST"])
def api_response_message():
    referer = request.headers.get("Referer")
    if referer is None:
      referer = request.args.get("referer")
    referer = referer.replace("//", "https://")
    # logging.info("____ referer: %s", referer)

    endpointUrl = referer + "/api/v1/conversation/send"
    message =  request.get_json(force=True)
    logging.info("____ message: %s", message)

    conversationId = extractConversationId(message)
    intent = extractDate2(message)

    if(len(intent) == 0):
        DateTime = "Es konnte kein Datum erkannt werden!"
    elif (checkDateFormat(intent) == False):
        DateTime = "Das Datumsformat ist nicht korrekt, es sollte das Format DD.MM.JJJJ haben."
    else:    
        DateTime = noticePeriod(intent)
    answer = createAnswer(conversationId, DateTime)
    try:
      # logging.info("____ endpointUrl: %s", endpointUrl)
      # logging.info("Request data: {0}".format(answer))
      response = requests.post(endpointUrl, data=answer, headers={'content-type': 'application/json'})
      # logging.info("Request endpoint response: {0}".format(response))
    except requests.exceptions.RequestException as e:
      logging.debug("Request endpoint error: {0}".format(e))
    return ('{}', 200)


@app.route("/dayMoveOut", methods=["POST"])
def api_response_message2():
    referer = request.headers.get("Referer")
    if referer is None:
      referer = request.args.get("referer")
    referer = referer.replace("//", "https://")
    # logging.info("____ referer: %s", referer)

    endpointUrl = referer + "/api/v1/conversation/send"
    message =  request.get_json(force=True)
    logging.info("____ message: %s", message)

    conversationId = extractConversationId(message)
    intent = extractDate1(message)

    if(len(intent) == 0):
        DateTime = "Es konnte kein Datum erkannt werden!"
    elif (checkDateFormat(intent) == False):
        DateTime = "Das Datumsformat ist nicht korrekt, es sollte das Format DD.MM.JJJJ haben."
    else:    
        DateTime = dayMoveOut(intent)
    answer = createAnswer(conversationId, DateTime)
    try:
      # logging.info("____ endpointUrl: %s", endpointUrl)
      # logging.info("Request data: {0}".format(answer))
      response = requests.post(endpointUrl, data=answer, headers={'content-type': 'application/json'})
      # logging.info("Request endpoint response: {0}".format(response))
    except requests.exceptions.RequestException as e:
      logging.debug("Request endpoint error: {0}".format(e))
    return ('{}', 200)

@app.route("/dayMoveOutFast", methods=["POST"])
def api_response_message6():
    referer = request.headers.get("Referer")
    if referer is None:
      referer = request.args.get("referer")
    referer = referer.replace("//", "https://")
    # logging.info("____ referer: %s", referer)

    endpointUrl = referer + "/api/v1/conversation/send"
    message =  request.get_json(force=True)
    logging.info("____ message: %s", message)

    conversationId = extractConversationId(message)
    #intent = extractDate1(message)

    DateTime = dayMoveOutFast()
    answer = createAnswer(conversationId, DateTime)
    try:
      # logging.info("____ endpointUrl: %s", endpointUrl)
      # logging.info("Request data: {0}".format(answer))
      response = requests.post(endpointUrl, data=answer, headers={'content-type': 'application/json'})
      # logging.info("Request endpoint response: {0}".format(response))
    except requests.exceptions.RequestException as e:
      logging.debug("Request endpoint error: {0}".format(e))
    return ('{}', 200)

@app.route("/noticePeriodSonder", methods=["POST"])
def api_response_message3():
    referer = request.headers.get("Referer")
    if referer is None:
      referer = request.args.get("referer")
    referer = referer.replace("//", "https://")
    # logging.info("____ referer: %s", referer)

    endpointUrl = referer + "/api/v1/conversation/send"
    message =  request.get_json(force=True)
    logging.info("____ message: %s", message)

    conversationId = extractConversationId(message)
    intent = extractDate3(message)

    if(len(intent) == 0):
        DateTime = "Es konnte kein Datum erkannt werden!"
    elif (checkDateFormat(intent) == False):
        DateTime = "Das Datumsformat ist nicht korrekt, es sollte das Format DD.MM.JJJJ haben."
    else:    
        DateTime = noticePeriodSonder(intent)
    answer = createAnswer(conversationId, DateTime)
    try:
      # logging.info("____ endpointUrl: %s", endpointUrl)
      # logging.info("Request data: {0}".format(answer))
      response = requests.post(endpointUrl, data=answer, headers={'content-type': 'application/json'})
      # logging.info("Request endpoint response: {0}".format(response))
    except requests.exceptions.RequestException as e:
      logging.debug("Request endpoint error: {0}".format(e))
    return ('{}', 200)

@app.route("/dayMoveOutSonder", methods=["POST"])
def api_response_message4():
    referer = request.headers.get("Referer")
    if referer is None:
      referer = request.args.get("referer")
    referer = referer.replace("//", "https://")
    # logging.info("____ referer: %s", referer)

    endpointUrl = referer + "/api/v1/conversation/send"
    message =  request.get_json(force=True)
    logging.info("____ message: %s", message)

    conversationId = extractConversationId(message)
    intent = extractDate4(message)

    if(len(intent) == 0):
        DateTime = "Es konnte kein Datum erkannt werden!"
    elif (checkDateFormat(intent) == False):
        DateTime = "Das Datumsformat ist nicht korrekt, es sollte das Format DD.MM.JJJJ haben."
    else:    
        DateTime = dayMoveOutSonder(intent)
    answer = createAnswer(conversationId, DateTime)
    try:
      # logging.info("____ endpointUrl: %s", endpointUrl)
      # logging.info("Request data: {0}".format(answer))
      response = requests.post(endpointUrl, data=answer, headers={'content-type': 'application/json'})
      # logging.info("Request endpoint response: {0}".format(response))
    except requests.exceptions.RequestException as e:
      logging.debug("Request endpoint error: {0}".format(e))
    return ('{}', 200)

@app.route("/dayMoveOutSonderFast", methods=["POST"])
def api_response_message5():
    referer = request.headers.get("Referer")
    if referer is None:
      referer = request.args.get("referer")
    referer = referer.replace("//", "https://")
    # logging.info("____ referer: %s", referer)

    endpointUrl = referer + "/api/v1/conversation/send"
    message =  request.get_json(force=True)
    logging.info("____ message: %s", message)

    conversationId = extractConversationId(message)
    #intent = extractDate1(message)

    DateTime = dayMoveOutSonderFast()
    answer = createAnswer(conversationId, DateTime)
    try:
      # logging.info("____ endpointUrl: %s", endpointUrl)
      # logging.info("Request data: {0}".format(answer))
      response = requests.post(endpointUrl, data=answer, headers={'content-type': 'application/json'})
      # logging.info("Request endpoint response: {0}".format(response))
    except requests.exceptions.RequestException as e:
      logging.debug("Request endpoint error: {0}".format(e))
    return ('{}', 200)

if __name__ == '__main__':
    app.run(debug=True)

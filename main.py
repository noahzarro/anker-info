from enum import Enum
from flask import Flask
import json
import requests
import schedule
import threading
import time

isTest = False

if isTest:
    ankerDataURL = "https://raw.githubusercontent.com/noahzarro/anker-data/refs/heads/testing/data.json" 
else:
    ankerDataURL = "https://raw.githubusercontent.com/noahzarro/anker-data/refs/heads/main/data.json"

class Promotion(Enum):
    HALF_PRICE = "50%"
    NONE = "None"
    OTHER = "Anker Aktion, aber nöd halbe Priis"

def weeklyRoutine(withAnnouncement=True):
    print("Running weekly routine")
    promotion = getPromotion()
    ankerData = getAnkerData()
    payload = buildPromotionPayload(promotion, ankerData)
    if withAnnouncement:
        announcePromotion(payload, ankerData)
    with open("payload.json", "w") as file:
        json.dump(payload, file)

def announcePromotion(payload, ankerData):
    print(ankerData["webhooks"])
    for webhook in ankerData["webhooks"]:
        print(webhook)
        try:
            requests.post(webhook, json=payload)
            print(f"Sent webhook to {webhook}")
        except Exception as e:
            print(f"Error sending webhook to {webhook}: {e}")

def buildPromotionPayload(promotion, ankerData):
    (promotionType, promotionString) = checkPromotion(promotion, ankerData["matchingPattern"])
    return {
        "hasPromotion": promotionType != Promotion.NONE,
        "isHalfPrice": promotionType == Promotion.HALF_PRICE,
        "promotionString": promotionString
    }

def checkPromotion(promotion, matchingPattern):
    if promotion == None or promotion.get("text", None) == None:
        return (Promotion.NONE, None)
    promotionString = promotion.get("text", None)
    if matchingPattern in promotionString:
        return (Promotion.HALF_PRICE, promotionString)
    return (Promotion.OTHER, promotionString)

def getAnkerData():
    response = requests.get(ankerDataURL)
    return response.json()

def getPromotion():
    if isTest:
        with open("test_promotion.json", "r") as file:
            response = json.load(file)
    else:
        response = requests.get("https://www.coop.ch/rest/v2/coopathome/products/3458809").json()
    return response.get("selectedPromotion", None)

def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

app = Flask("anker-api")

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def root():
    # welcome message
    return "<h1>Welcome to the Anker API!</h1><p>See the <a href='https://github.com/noahzarro/anker-info'>readme</a> for documentation</p>"

@app.route('/api/promotion')
def offerPromotion():
    with open("payload.json", "r") as file:
        return json.load(file)


def main():
    weeklyRoutine(withAnnouncement=False)
    schedule.every().monday.at("08:00", "Europe/Zurich").do(weeklyRoutine)
    threading.Thread(target=scheduler).start()
    app.run(debug=True, port=5000, host='0.0.0.0', use_reloader=False)

main()
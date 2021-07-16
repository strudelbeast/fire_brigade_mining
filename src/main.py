import requests
import traceback
import datetime as dt
from pymongo import collection, MongoClient
from dotenv import load_dotenv
from process_incident import save_to_db
from threading import Timer
import os
from typing import List

load_dotenv()
had_restart = False
BASE_URL = "https://infoscreen.florian10.info/OWS/wastlMobile/"

def load_data() -> List[dict]:
    active_incidents_resp = requests.get(
        BASE_URL + "getEinsatzAktiv.ashx",
        timeout=10)
    return active_incidents_resp.json().get('Einsatz')


def init_db() -> collection:
    client = MongoClient(
        host=os.environ.get('MONGO_HOST'),
        port=int(os.environ.get('MONGO_PORT')),
        username=os.environ.get('MONGO_USER'),
        password=os.environ.get('MONGO_PASSWORD'),
        maxPoolSize=50)
    collection = client['fw_incidents'][os.environ.get('DB_NAME')]
    return collection


def do(had_restart):
    # Repeat it every 60 seconds or with an cronjob.
    if (int(os.environ.get('REPEAT_MINUTE')) > 0):
        Timer(
            int(os.environ.get('REPEAT_MINUTE')) * 60,
            do,
            [had_restart]
        ).start()
    try:
        timestampStr = dt.datetime.now().strftime("[%d-%b-%Y %H:%M:%S]")

        collection = init_db()
        data = load_data()
        save_to_db(collection, data)
        print(timestampStr, "OK")
    except Exception as err:
        if not had_restart:
            timestampStr = dt.datetime.now().strftime("[%d-%b-%Y %H:%M:%S]")
            print(timestampStr, "An error occured!")
            traceback.print_exc()
            had_restart = True


if __name__ == '__main__':
    do(had_restart)

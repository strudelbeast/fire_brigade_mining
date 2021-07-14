import datetime as dt
import requests
from incident import Incident
from operating_resource import OperatingResource
from pymongo import collection
import json


def save_to_db(collection: collection, data: list):
    handle_ended_incidents(collection, data)

    for incident in data:
        incident_id = incident.get('i')
        incident_operating_ressources = load_incident_operating_ressources_from_incident_id(incident_id)

        item: Incident = collection.find_one({"_id": incident_id})

        new_incident = Incident(
            _id=incident_id,
            alarm_keyword=incident.get('a') if incident.get('a') != '' else None,
            alarm_description=incident.get('m'),
            place=incident.get('o') if incident.get('o') != '' else None,
            incident_number=incident_n_to_number(incident.get('n')),
            district=district_map_mappings[incident.get('b')],
            start_dtime=dt.datetime.strptime(incident.get('d') + ' ' + incident.get('t'), '%d.%m.%Y %H:%M:%S'),
            end_dtime=None,
            operating_ressources=incident_operating_ressources
        )

        if item is None:
            # Not in db
            collection.insert_one(new_incident.dict(by_alias=True))
        else:
            if item != new_incident:
                query = {'_id': incident_id}
                update = {'$set': new_incident.dict(by_alias=True)}
                collection.update_one(query, update, upsert=False)


# ======================== Util ======================== 

district_map_mappings = {
    '01': 'Amstetten',
    '02': 'Baden',
    '03': 'Bruck/Leitha',
    '04': 'Gänserndorf',
    '05': 'Gmünd',
    '061': 'Klosterneuburg',
    '062': 'Purkersdorf',
    '063': 'Schwechat',
    '07': 'Hollabrunn',
    '08': 'Horn',
    '09': 'Stockerau',
    '10': 'Krems',
    '11': 'Lilienfeld',
    '12': 'Melk',
    '13': 'Mistelbach',
    '14': 'Mödling',
    '15': 'Neunkirchen',
    '17': 'St. Pölten',
    '18': 'Scheibbs',
    '19': 'Tulln',
    '20': 'Waidhofen-thaya',
    '21': 'Wr. Neustadt',
    '22': 'Zwettl'
}

BASE_URL = "https://infoscreen.florian10.info/OWS/wastlMobile/"


def handle_ended_incidents(collection: collection, new_data: list):
    last_data = []
    try:
        with open('../last_data.json', 'r') as f:
            last_data = json.load(f)
    except FileNotFoundError:
        with open('../last_data.json', 'w'):
            pass
    ended_incidents = [x for x in last_data if x not in new_data]
    ended_query = {'_id': {'$in': [x.indicent_id for x in ended_incidents]}}
    ended_update = {'$set': {'end_dtime': dt.datetime.now()}}
    collection.update_one(ended_query, ended_update, upsert=False)

    with open('../last_data.json', 'w') as f:
        json.dump(new_data, f)


def incident_n_to_number(n: str) -> int:
    try:
        index_of_first_number = [x.isdigit() for x in n].index(True)
        return int(n[index_of_first_number:])
    except ValueError:
        return None
    except Exception as e:
        print(e)
        return None


def load_incident_operating_ressources_from_incident_id(incident_id: str) -> list[OperatingResource]:
    try:
        incident_resp = requests.get(
            BASE_URL + "geteinsatzdata.ashx",
            params={'id': incident_id},
            timeout=10)
        disposed: list[dict] = incident_resp.json()['Dispo']
        return list(map(
            lambda op_r: OperatingResource(
                _id=op_r.get('n'),
                disposition=get_datetime_from_censored_str(op_r.get('dt')),
                alert=(
                    get_datetime_from_censored_str(op_r.get('at')) if op_r.get('at') != 'own' else 'own') if op_r.get(
                    'at') != '' else None,
                move_out=get_datetime_from_censored_str(op_r.get('ot')) if op_r.get('ot') != '' else None,
                move_in=get_datetime_from_censored_str(op_r.get('it')) if op_r.get('it') != '' else None,
                dispatch_number=int(op_r.get('s'))
            ),
            disposed
        ))
    except Exception as e:
        print(e)
        return []


def get_datetime_from_censored_str(date_string: str) -> dt.datetime:
    date_string = date_string.replace('x', '0')
    return dt.datetime.strptime(date_string, '%d.%m.%Y %H:%M:%S')
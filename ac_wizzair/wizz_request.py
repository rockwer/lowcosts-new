import requests
import datetime
import json

def request_data(departureStation, arrivalStation, date_from, date_to, priceType):
    function_responce = {}
    function_responce_error = {}
    # request_url = "https://be.wizzair.com/7.7.4/Api/search/timetable"
    request_url = "https://be.wizzair.com/7.8.1/Api/search/timetable"
    head = {'content-type': 'application/json'}
    payload = {"flightList":[{
        "departureStation": departureStation,
        "arrivalStation": arrivalStation,
        "from": date_from,
        "to": date_to
        },{
        "departureStation": arrivalStation,
        "arrivalStation": departureStation,
        "from": date_from,
        "to": date_to
        }],
        "priceType": priceType,
        "adultCount": 1,
        "childCount": 0,
        "infantCount": 0
        }

    req = requests.post(request_url, headers=head, data=json.dumps(payload)).content
    req_decoded = req.decode('utf-8')

    try:
        req_json = json.loads(req_decoded)
        if 'validationCodes' in req_json:
            function_responce_error.update(req_json)
            return function_responce_error
        elif 'validationCodes' not in req_json:
            function_responce.update(req_json)
            return function_responce
    except ValueError:
        function_responce_error["Error"] = req_decoded
        return function_responce_error

    # print(function_responce_error)
    # print(function_responce)
    # return function_responce, function_responce_error
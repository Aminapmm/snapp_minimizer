from builtins import min

import requests
import json
from datetime import date
import time
import numpy as np
from termcolor import colored


def request(origin_lat, origin_long, dest_lat, dest_long):
    try:

        headers = {
            'authority': 'app.snapp.taxi',
            'content-type': 'application/json',
            'x-app-name': 'passenger-pwa',
            'x-app-version': '5.0.1',
            'authorization': 'Bearer eyJhbGciOiJSUzUxMiIsImtpZCI6Ino4YTRsNG9PRkVxZ2VoUllEQlpQK2ZwclBuTERMbWFia3NsT3hWVnBMTkUiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOlsicGFzc2VuZ2VyIl0sImVtYWlsIjoiYW1pbmFlNzcyQGdtYWlsLmNvbSIsImV4cCI6MTYzOTk0MzU4MSwiaWF0IjoxNjM4NzMzOTgxLCJpc3MiOjEsImp0aSI6Ijg5MzhVVllFRWV5WHRBSUFyQkJPU2FMVnIrelRDa0VhbG1sYzl6endVY0kiLCJzaWQiOiIyMXNkeUdaSnJscnFqREV4Y2xPczJKN0RqbGciLCJzdWIiOiJ5N3ZvME1HS0Frd2pSWlAifQ.no3zdbqJRxmeRrCsWDlUfuMVVYJ6UTPr_uPLhreuFgJCWhCOwPyh7YJYRV_VJwiK8BYosHmEcExD8sxX3B8Lyigbj0VY3GhsUHZ0DtUtutHbWkNU96gzD_5onqYiF4j3EVHcZZNNPom9wlTBA0nWgfEHW6hG-lgIOOuOxu7YX5fLCe8viRTBlxPFIpdnZ4BzQNFT0IQFutuINMGV3ujQvo7rC-5H3U2ZDtSW4yoCWbm2cf7PdzNsJumlHfTe4GN5DMs4It7XT5mlx6I3YP1PvBRiBiCrnfXyDK1B_h7TMPsdFkVNPiwIcnW_4g9SNcEdtX_P9OBo-q91xNPHqJ_VGX5cz9rD10jBEP8-mS7Mr4z4tYmMxS9vveFP3SVVup-n7fnmX8YTBKVfpcf8OTUTpYMltrEZtRAZaaelOuvAAyIx4I9e7y4Ac2hQOUx3mp9YJdeUbOPXYO4Hks1K_wRZCyJrv4g8EbXyFVV3df_IEabfXZoGyCCHrG4Hu_OT4s6vGeq3pruAYky1UBfy7xeJQQ10w8QpiXBSS-Gz9d_mrtdNiEPJt4rlvm3ua-qRa9q5HcWcqahasGg_JykrfDn8J0Kja34qHaLdwJO4675hptqHJipx2FdfFuSmuN7yfjUTVxpYQkD0GB4OnQZHWc4ZmIDGmQmUdva5B0vDGQZd_Ys',
            'locale': 'fa-IR',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'app-version': 'pwa',
            'accept': '*/*',
            'sec-gpc': '1',
            'origin': 'https://app.snapp.taxi',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://app.snapp.taxi/pre-ride?rideForm={%22options%22:{%22serviceType%22:1}}',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': '6aeffda4232f672ea9c7728c3f26e931=0ac32af42882168bc0f106d66f855698; b94e12faa7cc2207f53f7a102f98e4e9=a9b6fc5b15216c364e5b90f9e9bb4e69; df7bf34090025f8d898b3749fb588cb1=25c881ed48cac110a9ed6cbc107377ae; 9c34198dae104a4e1402a2f9c5f31c1b=59dc308e28727b7e808e26008a87a953; 7e8b7d8233619f305c0e68f414bf6d9b=99d9eead532b699b8ed38a78e649d7ac; 4e1a90f355b8196456cdcb3efe565cbd=9216441836f3e1acc98d51fb0f669022; 34b7ed1b00e796d0bcdc387e62021f03=2775572f2e21b5298d4502e2f81932ba; 7009208fd4d752045165a6638427b0d3=6ffbbf39e8f5b88ae446737e8ba3b755; Cookie_1=value'
        }

        # data = {"origin_lat":' + str(origin_lat) + ',"origin_lng":' + str(origin_long) + ',"destination_lat":' +
        # str(dest_lat) + ',"destination_lng":' + str(dest_long) + ',"waiting":None,"tag":0,"round_trip":False,
        # "voucher_code":None}
        """
        data = json.dumps(
            {"origin_lat": str(origin_lat), "origin_lng": str(origin_long), "destination_lat": str(dest_lat),
             "destination_lng": str(dest_long), "waiting": None, "tag": 0, "round_trip": False, "voucher_code": None})
             """
        payload = json.dumps({"points": [{"lat": str(origin_lat), "lng": str(origin_long)},
                                         {"lat": str(dest_lat), "lng": str(dest_long)}, None], "waiting": None,
                              "tag": 0, "round_trip": False, "voucher_code": None, "service_types": [1],
                              "hurry_price": None, "hurry_flag": None})

        response = requests.post("https://app.snapp.taxi/api/api-base/v2/passenger/newprice/s/6/0", headers=headers,
                                 data=payload)

        if response.status_code != 200:
            raise ValueError(response.content)

        data = json.loads(response.content)
        data = data["data"]
        service = data['prices']
        #print(service)
        m = int(10000000)
        for i in range(len(service)):
            final = int(service[i]['final'])
            m = int(np.min([m, final]))
        return m
        write_in_file(m)
    except Exception as e:
        print(colored(e, 'red'))
        write_in_file('something wrong')
        return 0


def write_in_file(price):
    fi = open("snapp.csv", 'a')
    fi.write(str(price) + ' , ' + str(date.today()) + ' , ' + str(time.strftime("%H:%M:%S", time.localtime())))
    fi.write('\n')
    fi.close()


def driver(origin, destination, r):
    print(time.strftime("%H:%M:%S", time.localtime()))
    res = 100000000
    price_list = []

    origin_lat = origin[0]
    origin_long = origin[1]
    dest_lat = destination[0]
    dest_long = destination[1]

    step = 20
    radius = r

    res_origin_lat = origin_lat
    res_origin_long = origin_long
    res_dest_long = dest_long
    res_dest_lat = dest_lat

    for a in range(-radius, radius, step):
        for b in range(-radius, radius, step):
            lat = origin_lat + round(a * .00001, 4)
            long = origin_long + round(b * .00001, 4)
            price = request(lat, long, dest_lat, dest_long)
            res = min(price, res)
            if price == res:
                res_origin_lat = lat
                res_origin_long = long
            price_list.append(price)

    for a in range(-radius, radius, step):
        for b in range(-radius, radius, step):
            lat = dest_lat + round(a * .00001, 4)
            long = dest_long + round(b * .00001, 4)
            price = request(res_origin_lat, res_origin_long, lat, long)

            res = min(price, res)
            if price == res:
                res_dest_lat = lat
                res_dest_long = long
            price_list.append(price)

    print(colored(str(time.strftime("%H:%M:%S", time.localtime())), 'yellow'), colored(res, 'green'))
    print('origin location \t' + str(res_origin_lat) + ',' + str(res_origin_long))
    print('dest location \t' + str(res_dest_lat) + ',' + str(res_dest_long))
    print('min price \t' + colored(min(price_list), 'red'))


if __name__ == '__main__':
    Home = [30.357989, 48.287269]
    pool = [30.335613868225963, 48.316866336784415]
    driver(Home, [30.33189500804493, 48.28650714818511], 100)

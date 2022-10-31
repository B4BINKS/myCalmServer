import json
from datetime import datetime

databaseFile, ratelimitTime, allowedRequest, keyRatelimit, ipRatelimit = '', '', '', '', ''

def Load():
    global databaseFile, ratelimitTime, allowedRequest, keyRatelimit, ipRatelimit
    try:
        with open('config.json', 'r', encoding='utf-8') as configFile:
            config = json.load(configFile)
            configToUse = config[0]['configToUse']
            if configToUse == 0:
                return {'success': False, 'message': 'Cant use config number 0 must be 0<', 'errorId': '001'}
            else:
                try:
                    config = config[configToUse] 
                    databaseFile = config['databaseFile']
                    ratelimitTime = config['ratelimitTime']
                    allowedRequest = config['allowedRequest']
                    keyRatelimit = config['keyRatelimit']
                    ipRatelimit = config['ipRatelimit'] 
                    return {'success': True}

                except IndexError:
                    return {'success': False, 'message': f'Config {configToUse} was not found', 'errorId': '002'}

    except json.decoder.JSONDecodeError:
        return {'success': False, 'message': 'Invalid json config !', 'errorId': '003'}
    except FileNotFoundError:
        return {'success': False, 'message': 'config.json file is missing !', 'errorId': '004'}

def newReq(ipAddr: str, timestamp: int, Key: str or int="None"):
    # Loading Database
    loadModule = Load()
    if not loadModule['success']:
        return loadModule['message']

    try:
        dbRead = json.load(open(databaseFile, 'r', encoding='utf-8'))
        try:
            dbRead[0]

        except IndexError:
            json.dump(json.loads('[{"ipAddr": "Default", "timestamp": 123456, "Key": "Default"}]'), open(databaseFile, 'w', encoding='utf-8'))
            dbRead = json.load(open(databaseFile, 'r', encoding='utf-8'))

    except FileNotFoundError:
        return {'success': False, 'message': 'Database file not found', 'errorId': '005'}

    except json.decoder.JSONDecodeError:
        json.dump(json.loads('[{"ipAddr": "Default", "timestamp": 123456, "Key": "Default"}]'), open(databaseFile, 'w', encoding='utf-8'))
        try:
            dbRead = json.load(open(databaseFile, 'r', encoding='utf-8'))

        except json.decoder.JSONDecodeError:
            return {'success': False, 'message': 'Invalid json database', 'errorId': '006'}

    def getAllKey(myjson, key, value: str or int): # https://stackoverflow.com/questions/14048948/how-to-find-a-particular-json-value-by-key (copied for time saving)
        if type(myjson) == str:
            myjson = json.loads(myjson)
        if type(myjson) is dict:
            for jsonkey in myjson:
                if type(myjson[jsonkey]) in (list, dict):
                    getAllKey(myjson[jsonkey], key, value)
                elif jsonkey == key:
                    if key == 'ipAddr':
                        if myjson[jsonkey] == value:
                            ipAddrList.append(myjson)
                    elif key == 'Key':
                        if myjson[jsonkey] == value:
                            keyList.append(myjson)
                        
        elif type(myjson) is list:
            for item in myjson:
                if type(item) in (list, dict):
                    getAllKey(item, key, value)

    global keyRatelimit, ipRatelimit
    ipRatelimited = False
    keyRatelimited = False

    if ipRatelimit:
        ipAddrList = []
        getAllKey(dbRead, 'ipAddr', ipAddr)
        IpcountReq = 1
        if not len(ipAddrList) == 0:
            timestampNow = round(datetime.now().timestamp())
            for log in ipAddrList:
                if timestampNow - log['timestamp'] > ratelimitTime:
                    pass
                else:
                    IpcountReq += 1
        if IpcountReq >= allowedRequest:
            ipRatelimited = True

    if keyRatelimit:
        keyList = []
        getAllKey(dbRead, 'Key', Key)
        KeycountReq = 1
        if not len(keyList) == 0:
            timestampNow = round(datetime.now().timestamp())
            for log in keyList:
                if timestampNow - log['timestamp'] > ratelimitTime:
                    pass
                else:
                    KeycountReq += 1


        if KeycountReq >= allowedRequest:
            keyRatelimited = True

    added = False

    if not ipRatelimited:
        if ipRatelimit:
            dbRead.append({"ipAddr": f"{ipAddr}", "timestamp": timestamp, "Key": f"{Key}"})
            json.dump(json.loads(json.dumps(dbRead)), open(databaseFile, 'w', encoding='utf-8'))
            added = True

    if not keyRatelimited:
        if keyRatelimit:
            if not added:
                dbRead.append({"ipAddr": f"{ipAddr}", "timestamp": timestamp, "Key": f"{Key}"})
                json.dump(json.loads(json.dumps(dbRead)), open(databaseFile, 'w', encoding='utf-8'))

    resp = {'success': True}
    if ipRatelimit:
        resp['ipRatelimit'] = {'ratelimited': ipRatelimited, 'reqCount': IpcountReq}



    if keyRatelimit:
        resp['keyRatelimit'] = {'ratelimited': keyRatelimited, 'reqCount': KeycountReq}

    return resp

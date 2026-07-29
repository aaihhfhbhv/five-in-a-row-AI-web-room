import urllib.request, json, sys

BASE = 'http://127.0.0.1:5001'

def post(path, payload):
    url = BASE + path
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.read().decode('utf-8')
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    print('create 8x8 room ->', post('/room/create', {'client_id':'owner1'}))
    print('create 15x15 room ->', post('/room/create', {'client_id':'owner15','width':15,'height':15}))

    # create a room and join
    import json
    res = post('/room/create', {'client_id':'hostA'})
    print('hostA create:', res)
    try:
        rid = json.loads(res)['roomId']
    except Exception as e:
        print('parse failed', e)
        sys.exit(1)
    print('join by guestB ->', post('/room/join', {'room_id': rid, 'client_id':'guestB'}))
    print('get room state ->', post('/room/state', {'room_id': rid}))

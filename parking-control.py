# parking control
# Author: Yan Ye <1603070001@svuca.edu>

import serial
import urllib.request
import json
from time import sleep

base_url = 'https://parking-server.mybluemix.net'
ep_hello = 'hello'
ep_terminal = 'terminal'
ep_space = 'space'

sp_file = '/dev/ttyACM0'
sp_baudrate = 9600

#PUT /hello
def hello():
    data = bytearray(json.dumps(tid), 'utf-8')
    req = urllib.request.Request(base_url + '/' + ep_hello, data=data)
    req.method = 'PUT'
    print(req.method + '\n' + str(data))

    resp = urllib.request.urlopen(req)

# POST /terminal
def request_new_tid():
    req = urllib.request.Request(base_url + '/' + ep_terminal)
    req.method = 'POST'

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.readline().decode('utf-8'))
    print(result)

    return result['terminalID']

#PUT /terminal
def put_terminal(terminal):
    data = bytearray(json.dumps(terminal), 'utf-8')
    req = urllib.request.Request(base_url + '/' + ep_terminal, data=data)
    req.method = 'PUT'
    print(req.method + '\n' + str(data))

    resp = urllib.request.urlopen(req)

#PUT /terminal/space
def put_space(space, occupied=True):
    data_dict = {'terminalID': tid, 'space': space, 'Occupation': occupied} 
    data = bytearray(json.dumps(data_dict), 'utf-8')
    req = urllib.request.Request(base_url + '/' + ep_terminal + '/' + ep_space, data=data)
    req.method = 'PUT'
    print(req.method + '\n' + str(data))

    resp = urllib.request.urlopen(req)

# Get registered terminal ID
id_filename = 'id.id'
tid = ''

try:
    id_file = open(id_filename, 'r+')
    tid = id_file.read()
    id_file.close()
except FileNotFoundError:
    tid = ''

if tid == '':
    tid = request_new_tid()
    id_file = open(id_filename, 'w')
    id_file.write(tid)
    id_file.close()

terminal = {'terminalID': tid, 'address': '4105 Fortune Dr, San Jose, CA', 'location':{'longtitude': 17.2338, 'latitude': 12.726}, 'space':{'Total': 200, 'Remaining':200}}

put_terminal(terminal)
#hello()


sp = serial.Serial(port=sp_file, baudrate=sp_baudrate)
print('Connected to Serial:' + sp_file + ' ' + str(sp_baudrate))

while True:
    if sp.in_waiting >= 0:
        line = sp.readline()
        print('Serial:' + str(line))
        fields = str(line).split(',')
        print(fields)
        #if fields[0] == 'Space':
        if True:
            space = int(fields[1])
            if fields[2].startswith('full'):
                put_space(space, True)
            else:
                put_space(space, False)

    sleep(0.01)


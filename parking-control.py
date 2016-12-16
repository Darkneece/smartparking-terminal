# parking control
# Author: Yan Ye <1603070001@svuca.edu>

import serial
import urllib.request
import json
from time import sleep

base_url = 'https://parking-server.mybluemix.net'
ep_hello = 'hello'
ep_terminal = 'terminal'

sp_file = '/dev/ttyACM0'
sp_baudrate = 115200

# POST /terminal
def request_new_tid():
    req = urllib.request.Request(base_url + '/' + ep_terminal)
    req.method = 'POST'

    with urllib.request.urlopen(req) as response:
        result = json.loads(response.readline().decode('utf-8'))
    print(result)

    return result

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
    id_file.write(json.dumps(tid))
    id_file.close()
else: # PUT /hello
    data = bytearray(json.dumps(tid), 'utf-8')
    req = urllib.request.Request(base_url + '/' + ep_hello, data=data)
    req.method = 'PUT'
    
    print(req.method + '\n' + str(data))

    resp = urllib.request.urlopen(req)

sp = serial.Serial(port=sp_file, baudrate=sp_baudrate)
print('Connected to Serial:' + sp_file + ' ' + str(sp_baudrate))

while True:
    if sp.in_waiting >= 0:
        line = sp.readline()
        print('Serial:' + str(line))

    sleep(0.01)


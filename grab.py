import subprocess
import json
import http.client as http
import base64
try:
    arch = subprocess.run(['uname', '-m'])
except FileNotFoundError:
    arch = None
server_path = "/rasp_screenshot/server.php"
hostname = subprocess.check_output(['hostname', '-I'])
hostname = hostname.decode()[:-2]
server_ip = "192.168.17.88"
en = False
time = 5
thumb_perc = 50
quality = 50
headers = {'Content-type': 'application/json'}
while arch:
    subprocess.run(['sleep', time])
    _obj = {
        'hostname': hostname,
        'file': ""
    }
    if en == True:
        subprocess.run(['scrot', '--thumb', thumb_perc, '-q', quality, '{}.jpg'.format(hostname)])
        with open('{}.jpg'.format(hostname), 'rb') as f:
            img = f.read()
            img = base64.b64encode(img).decode()
            _obj['file'] = json.dumps(img)
        subprocess.run(['rm', '{}.jpg'.format(hostname)])
    conn = http.HTTPConnection("{}:80".format(server_ip))
    conn.request("POST", server_path, _obj, headers)
    json_flags = conn.getresponse().read().decode()
    flags = json.loads(json_flags)
    en = flags['en']
    time = flags['time']

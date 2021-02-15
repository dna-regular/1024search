import json

def get_json_conf():
    with open('/usr/local/etc/1024.json', 'r') as f:
        s = f.read()
        f.close()
        j = json.loads(s)
        return j

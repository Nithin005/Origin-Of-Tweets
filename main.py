import json
import sys

if(len(sys.argv) < 2):
    print('usage: main.py [--mitm] [--backend]')
    sys.exit(1)

param = sys.argv[1] 

from backend.searz.webapp import server as backend_server
from MITM.webserver import server as mitm_server

config = {}

with open('config.json') as f:
    config = json.load(f)

if(param == '--mitm'):
    mitm_server.run(port=config['mitm'])
elif(param == '--backend'):
    backend_server.run(port=config['backend'])
else:
    print('usage: main.py [--mitm] [--backend]')
    sys.exit(1)

# if __name__ == '__main__':
# main()
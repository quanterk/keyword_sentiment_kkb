from gevent import monkey
monkey.patch_all()

import getopt
import sys
from gevent.pool import Pool
from gevent.pywsgi import WSGIServer
from bottle import Bottle

addr, port = '127.0.0.1', 8898
opts, _ = getopt.getopt(sys.argv[1:], "b:")
for opt, value in opts:
    if opt == '-b':
        addr, port = value.split(":")

app = Bottle()
pool = Pool(256)
server = WSGIServer((addr, int(port)), app, spawn=pool)
server.backlog = 256
server.max_accept = 30000
print('ok')
server.serve_forever()
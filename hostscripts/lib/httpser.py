
"""
http GET api server

sample usage:
h = HttpSer({"/ts": lambda: print("TS")})
def main():
    while True:
        h.update()
try:
    main()
except KeyboardInterrupt:
    h.close()
    print("\nclosed")

"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import listdir
from os.path import splitext
from shutil import copyfileobj

PORT = 5001

MIME = {"html": "text/html",
        "js": "text/javascript",
        "css": "text/css"}

WEB_PATH = "./lib/web"

class HttpSer:
    """http api server"""
    def __init__(self, urlmap, addr="127.0.0.1", port=PORT):

        class _Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                ''' method that gets call when GET is recived'''

                if self.path[1:] in listdir(WEB_PATH):
                    self.send_response(200)
                    SURFIX = splitext(self.path)[1]
                    if SURFIX in MIME:
                        self.send_header("Content-Type", MIME[SURFIX])
                    self.end_headers()
                    copyfileobj(open(WEB_PATH + self.path, 'rb'), self.wfile)
                    return

                if self.path in urlmap:
                    rlt = urlmap[self.path]()
                    msg = rlt if rlt else "OK"
                    retcode = 200
                else:
                    msg = "NO_MATCH"
                    retcode = 404

                self.send_response(retcode)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(msg.encode())

        httpd = HTTPServer((addr, port), _Handler)

        # don't block
        httpd.timeout = 0
        self.ser = httpd

    def update(self):
        """ handle api request without blocking"""
        self.ser.handle_request()

    def close(self):
        """ close internal http server """
        self.ser.server_close()

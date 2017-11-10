
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

PORT = 5001

class HttpSer:
    """http api server"""
    def __init__(self, urlmap, addr="127.0.0.1", port=PORT):

        class _Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                ''' method that gets call when GET is recived'''
                self.send_response(200)
                self.end_headers()

                if self.path in urlmap:
                    urlmap[self.path]()
                    self.wfile.write("OK".encode())
                else:
                    self.wfile.write("NO_MATCH".encode())

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

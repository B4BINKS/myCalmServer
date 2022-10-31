from http.server import BaseHTTPRequestHandler, HTTPServer
from ratelimit import newReq
from datetime import datetime
from urllib.parse import urlparse, parse_qs

hostName = "127.0.0.1"
serverPort = 1337

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if 'favicon.ico' in self.path:
            pass
        else:
            try:
                query_components = parse_qs(urlparse(self.path).query)
                Key = query_components['key'][0]
                ipAddr = self.client_address[0]
                timestamp = round(datetime.now().timestamp())
                try:
                    ratelimitCheck = newReq(ipAddr=str(ipAddr),timestamp=int(timestamp),Key=Key)
                    if ratelimitCheck['success']:
                        if ratelimitCheck['ipRatelimit']['ratelimited']: # if you make ipRatelimit: true in config else if you make keyRatelimit: true in config put keyRatelimit
                            self.wfile.write(bytes(
                                'You have been ratelimited',"utf-8"
                                ))
                        else:
                            self.wfile.write(bytes(
                                'You are not ratelimited :)',"utf-8"
                                ))
                    else:
                        errorId = ratelimitCheck['errorId']
                        self.wfile.write(bytes(
                                'Hum, a problem occured please contact a admin Error ID: '+errorId,"utf-8"
                                ))
                except KeyError:
                    self.wfile.write(bytes(
                                'Hum, a problem occured please contact a admin Error ID: 1337',"utf-8"
                                ))
            except KeyError:
                self.wfile.write(bytes(
                    'Key parameter is missing.',"utf-8"
                    ))


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

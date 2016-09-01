#Author Mike Terranova

import BaseHTTPServer
import urlparse
import json
import requests

def run_while_true(server_class=BaseHTTPServer.HTTPServer, handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
    server_address = ('', )
    httpd = server_class(server_address, handler_class)
    while True:
        httpd.handle_request()

class handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                'HEADERS RECEIVED:',
                ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        return
    
    def parse_POST(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

    def do_POST(self):
        self.parse_POST()
        message = json.loads(self.data_string)
        if not 'text' in message:
            return
        text = message['text']
        print "INCOMING TEXT: " + text
        if 'Meeseeks' in text:
            payload = {"bot_id":"","text":"YESSIRREE!"}
            r = requests.post('https://api.groupme.com/v3/bots/post', data=json.dumps(payload))
            print "did it"
        else:
            print 'didnt do it'
            return

run_while_true(BaseHTTPServer.HTTPServer,handler)

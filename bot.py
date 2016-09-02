import BaseHTTPServer
import urlparse
import json
import requests
from random import randint

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
        text = message['text'].lower()
        if message['sender_type'] == 'bot':
            return
        print "INCOMING TEXT: " + message['text']
        if 'mr.meeseeks' in text:
            payload = {"bot_id":""}
            if 'hello' in text:
                payload["text"] = "Hi I'm Mr.Meeseeks! Look at me!"
                print '> said hello'
            if 'show' in text and 'me' in text and 'what' in text:
                payload["text"] = "I'm Mr. Meeseeks! Commands are:\nHello\ncan you\ncode \n google ( Mr.Meeseeks google ...\n trying)"
                print '> showed commands'
            if 'can' in text and 'you' in text:
                x = randint(1,2)
                if x == 1:
                    y = 'CAAAANNNN DOOoooOO'
                else: 
                    y = "YESSIRREEE"
                payload["text"] = y
                print '> can do'
            if 'google' in text:
                payload['text'] = " Look at me! Heres your search!\n" + lmgtfy(text)
                print "googled that for ya"
            if 'trying' in text:
                payload['text'] = "ooooooooooooo he's trying!" 
                print 'oo tryin'
            if 'code' in text:
                payload['text'] = "I'm Mr.Meeseeks! Look at me! https://github.com/miket1113/Meeseeksbot"
                print '> showed github'

            if 'text' in payload:
                r = requests.post('https://api.groupme.com/v3/bots/post', data=json.dumps(payload))

def lmgtfy(text):
    searchText = []
    baseURL = "http://lmgtfy.com/?q="
    for word in text.split(' '):
        searchText.append(word)
    searchText.pop(0)
    searchText.pop(0)
    for searchWord in searchText:
        baseURL+=searchWord
        baseURL+='+'
    newURL = baseURL
    return newURL





run_while_true(BaseHTTPServer.HTTPServer,handler)

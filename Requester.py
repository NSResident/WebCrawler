import requests
import re
import threading
import time
import socket

class Requester:
    host = ""
    user_agent = "CSE361-KappaBot"

    def __init__(self, domain):
        self.host = domain.replace('http://', '')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(4)
        # Handle if connection not made
        self.sock.connect((self.host, 80))
        if self.sock == -1:
            print -1 

    def __del__(self):
        self.sock.close()

    def get(self, url):
        path =  url[url.find('/')+1:]
        path = path[path.find('/')+1:]
        path = path[path.find('/'):]
        if path == '' or path[0] != '/':
            path = '/'
        header = ("GET {} HTTP/1.1\r\n" 
                    "Host: {}\r\n"
                    "User-Agent: {}\r\n" 
                    "Pragma: no-cache\r\n"
                    "Accept: text/plain, text/html\r\n" 
                    "Accept-Encoding: \r\n"
                    "Accept-Language: en-US\r\n" 
                    "Connection: Keep-Alive\r\n\r\n").format(path,self.host,self.user_agent)

        #"Cache-Control: no-cache, no-store, must-revalidate\r\n"
        print header
        self.sock.send(header)
        response_header = ""
        response = ""
        status_code = ""
        total = 0
        initial_response = self.sock.recv(4096)
        #print initial_response
        #Parse for header fields 
        for s in initial_response.splitlines():
            response_header += s
            response_header += "\n"
            field =  s.strip().split(': ')
            if field[0] == 'Content-Length':
               total = int(field[1])
            elif 'HTTP/1.1' in field[0]:
                status_code = field[0].split()[1]
            elif field[0] == '':
                break
            #else if field[0] == 'Transfer-Encoding':
            #    if field[1] == 'chunked':

        
        response = initial_response[initial_response.find('<html'):]
        #Handle Error Codes
        pattern = re.compile("([3-5]..)")
        if(pattern.match(status_code)):
            return -1 

        self.sock.send(header)
        current_amount = len(response) 
        #while current_amount < total:
        try:
            while True:
                latest_response  = self.sock.recv(1024)
                current_amount = current_amount + len(latest_response)
                response += latest_response
        except:
            #find HTML or html
            response = response[:response.find('</HTML>')+7]
        #Return Object:
        # URL
        # cookies
        # respone body
        # **user_name
        # **password
        result = postInfo(url, cookies, response)
        return result 

    def post(self, postInfo):
        #iterating through fields and adding to body of post
        body = ""

        header = ("POST {} HTTP/1.0\r\n"
                "Host: {}\r\n\r\n"
                "{}\r\n").format(postInfo.url,self.host,body)
        print header
        response = ""
        try:
            self.sock.send(header)
            while True:
                latest_response  = self.sock.recv(1024)
                response += latest_response
        except:
            #find HTML or html
            response = response[:response.find('</HTML>')+7]
        return response

#path = 'http://austinchildrensacademy.org'
r =  Requester('http://www.badstore.net')
#path = 'http://austinchildrensacademy.org/about-aca/'
#print r.get('http://wwww.badstore.net/cgi-bin/badstore.cgi')
#print requests.get('http://www.badstore.net/cgi-bin/badstore.cgi?action=loginregister').content

print '\n'
#print r.get('http://www.badstore.net/cgi-bin/badstore.cgi?action=loginregister')
print r.post('/cgi-bin/badstore.cgi?action=loginregister','','')


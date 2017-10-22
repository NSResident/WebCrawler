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
        self.sock.settimeout(7)
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
        if path[0] != '/':
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
        self.sock.send(header)
        response_header = ""
        response = ""
        status_code = ""
        total = 0
        initial_response = self.sock.recv(4096)
        print initial_response
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
        while current_amount < total:
            latest_response  = self.sock.recv(1024)
            current_amount = current_amount + len(latest_response)
            response += latest_response
        response = response[:response.find('</html>')+7]
        return response 

    def post(self, url, username, password):
        print response
        return

#path = 'queensfarm.org'
#r =  Requester(path)
#path = '/'
#print r.get(path)


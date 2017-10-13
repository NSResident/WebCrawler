import re
import threading
import time
import socket

class Requester:
    host = ""
    user_agent = "CSE361-KappaBot"

    def __init__(self, domain):
        self.host = domain
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Handle if connection not made
        self.sock.connect((domain, 80))

    def __del__(self):
        self.sock.close()

    def get(self, url):
        #path =  url[url.find('/')+1:]
        #path = path[path.find('/')+1:]
        #path = path[path.find('/'):]
        #if path[0] != '/':
        #    path = '/'
        header = ("GET {} HTTP/1.1\r\n" 
                    "Host: {}\r\n"
                    "User-Agent:{}\r\n" 
                    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n" 
                    "Accept-Language: en-US,en\r\n" 
                    "Connection: Keep-Alive\r\n\r\n").format(url,self.host,self.user_agent)

        print header
        self.sock.send(header)
        response_header = ""
        response = ""
        status_code = ""
        total = 0
        initial_response = self.sock.recv(1024)

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
            return "Error"

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

path = 'animals.mom.me'
r =  Requester(path)
path = 'http://animals.mom.me'
print r.get(path)


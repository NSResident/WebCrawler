import requests
import re
import threading
import time
import socket
from urlparse import urlparse
from bs4 import BeautifulSoup
from postInfo import postInfo


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
        #path =  url[url.find('/')+1:]
        #path = path[path.find('/')+1:]
        #path = path[path.find('/'):]
        path = urlparse(url).path
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
        #Parse Cookies
        cookies = {}
        for field in response_header.split('\n'):
            if "Set-Cookie:" in  field:
                values = field[len("Set-Cookie: "):].split(';')
                pair = values[0].split('=')
                cookies[pair[0]] = pair[1]
        # print cookies
        # print response_header
        response = initial_response[initial_response.find('<html'):]
        #Handle Error Codes
        pattern = re.compile("([3-5]..)")
        if(pattern.match(status_code)):
            return -1

        self.sock.send(header)
        current_amount = len(response)
        #while current_amount < total:
        try:
            latest_response = self.sock.recv(1024)
            while latest_response.strip():
                current_amount = current_amount + len(latest_response)
                response += latest_response
                latest_response  = self.sock.recv(1024)
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

    def post(self, postInfo, fields):
        #iterating through fields and adding to body of post
        #field dictionary in post
        path = urlparse(postInfo.url).path
        # Build request body
        body = ""
        for key in fields.keys():
            body += "&"
            body += str(key) + "=" + str(fields[key])
        body = body[1:]

        header = ("POST {} HTTP/1.0\r\n"
                "Host: {}\r\n"
                "User-Agent: {}\r\n"
                "Accept: text/plain, text/html\r\n"
                "Accept-Encoding: \r\n"
                "Content-Type: application/x-www-form-urlencoded\r\n"
                "Content-Length: {}\r\n"
                "Connection: Keep-Alive\r\n"
                ).format(path,self.host,self.user_agent,len(body))
        print postInfo.cookies
        if postInfo.cookies:
            cookie_string = ""
            for key in postInfo.cookies.keys():
                cookie_string += key + "=" + postInfo.cookies[key]+ ';'
                cookie_string += "\r\n"
            header += "Cookie: {}".format(cookie_string)
        header += "\r\n"
        header += body
        # print header
        response = ""
        try:
            self.sock.send(header)
            latest_response = self.sock.recv(1024)
            while latest_response.strip():
                response += latest_response
                latest_response  = self.sock.recv(1024)
        except:
            #find HTML or html
            response = response[:response.find('</HTML>')+7]
        return response
#Returns Dictionary of correct credentials if successful bruteforce.
#Unsuccessful Bruteforces return null
def bruteForce(self, url, username, keywords):
   postInfo = get(url)
   #Attempt to login
   query = {}
   query[postInfo.username_field] = username
   for password in keywords:
       query[password_field] = password
       response = post(postInfo, query)
       forms = soup.findAll("form")
       if soup.findAll(type ="password"):
           #False if Login successful(supposedly)
           continue
       else:
           return {"Username": username, "Password": password}
   return None

#path = 'http://austinchildrensacademy.org'
#r =  Requester('http://shop.nhl.com')
#info = r.get('http://shop.nhl.com')
#r.post(info, {"Hello":"World", "foo":"bar"})
#path = 'http://austinchildrensacademy.org/about-aca/'
#print r.get('http://wwww.badstore.net/cgi-bin/badstore.cgi')
#print requests.get('http://www.badstore.net/cgi-bin/badstore.cgi?action=loginregister').content

#print '\n'
#print r.get('http://www.badstore.net/cgi-bin/badstore.cgi?action=loginregister')
#print r.post('/cgi-bin/badstore.cgi?action=loginregister','','')


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
    const = ("GET {0} HTTP/1.1\r\n"
                    "Host: {1}\r\n"
                    "User-Agent: {2}\r\n"
                    "Pragma: no-cache\r\n"
                    "Accept: text/plain, text/html\r\n"
                    "Accept-Language: en-US\r\n"
                    "Connection: Keep-Alive\r\n")
    def __init__(self, domain):
        self.host = domain.replace('http://', '')
        print self.host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(1)
        # Handle if connection not made
        self.sock.connect((self.host, 80))
        if self.sock == -1:
            print -1

    def __del__(self):
        self.sock.close()

    def get(self, url, cookies=None):
        # path =  url[url.find('/')+1:]
        # path = path[path.find('/')+1:]
        # path = path[path.find('/'):]
        path = urlparse(url).path.rstrip()
        print path

        header = self.const.format(str(path),self.host,self.user_agent)

        print header
        #"Cache-Control: no-cache, no-store, must-revalidate\r\n"
        if cookies:
            cookie_string = ""
            for key in cookies.keys():
                cookie_string += key + "=" + cookies[key]+ ';'
                cookie_string += " "
            header += "Cookie: {}".format(cookie_string[:-2])+"\r\n"
        header += "\r\n"
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
            response = response[:response.find('</html>')+7]

        #Return Object:
        # URL
        # cookies
        # respone body
        # **user_name
        # **password
        result = postInfo(url, cookies, response)
        return result

    def post(self, info, fields):
        #iterating through fields and adding to body of post
        #field dictionary in post
        path = urlparse(info.url).path
        # Build request body
        body = ""
        for key in fields.keys():
            body += "&"
            body += str(key) + "=" + str(fields[key])
        body = body[1:]

        header = ("POST {} HTTP/1.1\r\n"
                "Host: {}\r\n"
                "User-Agent: {}\r\n"
                "Accept: text/plain, text/html\r\n"
                "Content-Type: application/x-www-form-urlencoded\r\n"
                "Content-Length: {}\r\n"
                "Connection: Keep-Alive\r\n"
                ).format(path,self.host,self.user_agent,len(body))
        if info.cookies:
            cookie_string = ""
            for key in info.cookies.keys():
                cookie_string += key + "=" + info.cookies[key]+ ';'
                cookie_string += " "
            header += "Cookie: {}".format(cookie_string[:-2])+"\r\n"
        header += "\r\n"
        header += body + "\r\n\r\n"
        # print header
        print header
        response = ""
        try:
            self.sock.send(header)
            latest_response = self.sock.recv(1024)
            while latest_response.strip():
                response += latest_response
                latest_response  = self.sock.recv(1024)
        except:
            #find HTML or html
            if response.find("<html>") != -1:
                response = response[:response.find('</html>')+7]
            print response
            return response

#Returns Dictionary of correct credentials if successful bruteforce.
#Unsuccessful Bruteforces return null
    def bruteForce(self, url, username, keywords, action, login_field, password_field):
        #r = Requester(url)
        info  = self.get(url)
        #Assume action doesnt have a slash
        info.url = info.url+action[1:]
        #Attempt to login
        query = {}
        query[login_field] = username
        for password in keywords:
            query[password_field] = password
            r = Requester(self.host)
            response = r.post(info, query)
            response_code = response.splitlines()[0]
            redirect = re.search('3\d{2}',response_code)
            if redirect:
                new_host_index = response.find("Location: ") + len("Location: ")
                new_host_end = response[new_host_index:].find('\n') + new_host_index
                new_host = response[new_host_index:new_host_end]
                new_host = urlparse(new_host).path
                new_host = 'http://' + r.host + '/' + new_host
                response = r.get(new_host, cookies=info.cookies)
                print response.response_body
            #If response is redirect (3**) then call get on the url at location: xxxx
            #Else its probably js and just check the page returned for password
            soup = BeautifulSoup(response.response_body, "html.parser")
            if soup.findAll(type ="password"):
                #False if Login successful(supposedly)
                print response
                continue
            else:
                return {"Username": username, "Password": password}
        return None

#path = 'http://austinchildrensacademy.org'
#r =  Requester('http://www.badstore.net')
#info = r.get('http://shop.nhl.com')
#r.post(info, {"Hello":"World", "foo":"bar"})
#path = 'http://austinchildrensacademy.org/about-aca/'
#print r.get('http://wwww.badstore.net/cgi-bin/badstore.cgi')
#print requests.get('http://www.badstore.net/cgi-bin/badstore.cgi?action=loginregister').content

#print '\n'
#print r.get('http://www.badstore.net/cgi-bin/badstore.cgi?action=loginregister')
#info = postInfo('/cgi-bin/badstore.cgi?action=loginregister','','')
#print r.post(info,fields = {'email': 'admin\' AND 1=1 -- ', 'password': ''})


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
        
    def get(self, url = '/'):
        #Parse url for path
        header = ("GET {} HTTP/1.1\r\n" 
                    "Host: {}\r\n"
                    "User-Agent:{}\r\n" 
                    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n" 
                    "Accept-Language: en-US,en\r\n" 
                    "Connection: Keep-Alive\r\n\r\n").format(url,self.host,self.user_agent)

        print header
        self.sock.send(header)
        #Create loop to keep receiving messages until a timeout where no more messages are read
        response = self.sock.recv(8192)

        # Check error code and handle 404/500 errors
        # Parse reponse for payload -> html_page

        return response 

    def post(self, url, username, password):
        return

r =  Requester("nexon.net")
print r.get()

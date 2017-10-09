import socket

class Requester:
    host = ""
    user_agent = "CSE361-KappaBot"

    def __init__(self, user_agent, domain):
        self.host = domain
        self.user_agent = user_agent
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Handle if connection not made
        self.sock.connect((self.host, 443))

    def get(self, url = '\\'):
        #Parse url for path
        path = ""
        header = "GET" + path + " HTTP/1.1\n"+"Host: " \
                + self.host + '\n'+"User-Agent: " \
                + self.user_agent + '\n' \
                + "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8 \n" \
                + "Accept-Language: en-US,en\n" \
                + "Connection: keep-alive\n"
        print header
        self.sock.send(header)
        #Handle if nothing comes back(?) 
        response = self.sock.recv(4096)

        # Check error code and handle 404/500 errors
        # Parse reponse for payload -> html_page

        return response 

    def post(url):
        return

r =  Requester("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0","superdry.com")
print r.get()

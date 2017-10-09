import socket

class Requester:
    host = ""
    user_agent = "CSE361-KappaBot"

    def __init__(self, user_agent, host):
        self.host = host
        self.user_agent = user_agent

    def get(url):
        #Parse url for path
        path = ""
        header = "HEAD" + path + " HTTP/1.1\n"
                +"Host: " + host + '\n'
                +"User-Agent: " + user_agent + '\n'
                +"Accept-Language: en-US,en"+'\n'
       
       sock = socket(AF_INET, SOCK_STREAM)
       # Handle if connection not made
       sock.connect(host, 443)
       sock.send(header)
       #Handle if nothing comes back(?) 
       response = sock.recv(4096)

       # Check error code and handle 404/500 errors
       # Parse reponse for payload -> html_page
       
       return html_page

    def post(url):
        return

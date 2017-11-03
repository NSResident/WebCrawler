class postInfo:
    url = ""
    cookies = ""
    response_body = ""

    def __init__(self, url, cookies, response_body):
        self.url = url
        self.cookies = cookies
        self.response_body = response_body

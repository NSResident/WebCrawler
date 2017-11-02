class postInfo:
    url = ""
    cookies = ""
    response_body = ""
    username_field = "username"
    password_field = "password"

    def __init__(self, url, cookies, response_body):
        self.url = url
        self.cookies = cookies
        self.response_body = response_body

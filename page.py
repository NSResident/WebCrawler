class Page:
    url_list = []
    html_text = ""
    login_url = ""
    depth = 0
    def __init__(self, urls, text, login_url):
        self.urL_list = urls
        for url in urls:
            self.url_list.append(url)
        self.html_text = text
        self.login_url = login_url

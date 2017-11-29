from page import Page
from url_node import URL_Node
from Queue import Queue
from Stack import Stack
from bs4 import BeautifulSoup
# from threading import Thread
from Requester import Requester
from urlparse import urlparse

class Crawler:
    # Variables from config
    search_flag = 0
    max_pages = 1
    max_depth = 1
    login_name = ""
    password_name = ""
    login_form = {}
    #Form Action
    action = ""
    # Queue for page objects
    parserQueue = Queue()
    # List of keywords
    word_dict = []
    # Dictoinary of visited Linkes
    link_dict = {}
    # Login url
    login_url= ""
    # Starting url
    starting_url = ""
    #starting_url = "http://austinchildrensacademy.org"
    parse_subdomains = False
    parse_robots = False
    requester = None

    def __init__(self, page_max, depth_max, search_type, subdom, robots):
        self.max_pages = page_max
        self.max_depth = depth_max
        self.search_flag = search_type
        self.parse_subdomains = subdom
        self.parse_robots = robots

    def searchStart(self, initial_url):
        visited_urls = self.searchInit(initial_url)
        if self.parse_subdomains:
            self.subdomainSearch()
        if self.parse_robots:
            self.robotSearch()
        return visited_urls

    def searchInit(self,initial_url):
        # :ssword:q Makes q/s
        # Add first url to q/s
        self.starting_url = initial_url
        url_list = []
        main_domain = urlparse(initial_url).netloc
        try:
            self.requester = Requester(initial_url)
        except:
            return
        
        first_url = URL_Node(initial_url+'/', 0)
        if self.link_dict.get(first_url.url):
            del self.link_dict[first_url.url]
        if self.search_flag == 0:
            self.crawlerQueue = Queue()
            self.crawlerQueue.put(first_url)
        else:
            self.crawlerStack = Stack()
            self.crawlerStack.push(first_url)
        # Page counter
        counter = self.max_pages
        # Make Q for Parser
        while counter > 0:
            
            # Take from q/s and check for domain, if it does not continue
            # Also added if queue was empty to cover edge case of q/s hanging when max_pages < available pages
            if self.search_flag == 0:
                if self.crawlerQueue.empty():
                    break
                nextUrl = self.crawlerQueue.get()
            else:
                if self.crawlerStack.is_empty():
                    break
                nextUrl = self.crawlerStack.pop()

            # Stay within the domain of initial url
            # Needs to work for AA.BBB.CCC.com
            
            if urlparse(nextUrl.url).netloc != main_domain:
                continue
            # Call search and return page object
            # 
            
            url_list.append(nextUrl.url)
            #
            if self.link_dict.get(nextUrl.url):
                
                continue
            next_page = self.search(nextUrl)
            
            self.link_dict[nextUrl.url] = nextUrl.url
            if next_page:
                None
                #
            # 
            # Check if object was empty from page error Edit to check for response
            if next_page:
                if next_page.url_list and nextUrl.depth < self.max_depth:
                    # Put all links into q/s
                    for url_item in next_page.url_list:
                        next_node = URL_Node(url_item, nextUrl.depth + 1)
                        # Ignore repeated links when crawling
                        if self.link_dict.get(next_node.url) is None:
                            if self.search_flag == 0:
                                self.crawlerQueue.put(next_node)
                            else:
                                self.crawlerStack.push(next_node)
                self.parserQueue.put(next_page)
            counter = counter - 1
        self.parser()
        return url_list


    # Searches url and returns a "page" of text and links
    def search(self, domain):
        # Get Text
        # Change  requests to use own get
        #html_text = requests.request('GET', domain.url, timeout=7).text
        
        try:
            html_text = self.requester.get(domain.url)
        except:
            html_text = -1
        if html_text == -1:
            return None
        else:
            html_text = html_text.response_body
        soup = BeautifulSoup(html_text, 'html.parser')
        # Get links
        link_list = []
        for link in soup.find_all('a'):
            #
            if link.get('href') is not None and "http" in link.get('href'):
                link_list.append(link.get('href'))

        # Check for login
        if soup.find_all(type='password'):
            self.login_url = domain.url
            forms = soup.find_all('form')
            for form in forms:
                if 'password' in str(form):
                    inputs = form.find_all('input')
                    for i in range(len(inputs)):
                        input_string = str(inputs[i])
                        if 'type="hidden' in input_string:
                            field_name_index = input_string.find('name="') + 6
                            field_name_end = field_name_index + input_string[field_name_index:].find('"')
                            field_name = input_string[field_name_index:field_name_end]
                            field_value_index = input_string.find('value="') + 7
                            field_value_end = field_value_index + input_string[field_value_index:].find('"')
                            field_value = input_string[field_value_index:field_value_end]
                            self.login_form[field_name] = field_value
                        if 'password' in input_string: #password_input
                            login_string = str(inputs[i-1]) #Guessing here
                            login_name_index = login_string.find('name="') + 6
                            login_name_end = login_name_index+login_string[login_name_index:].find('"')
                            self.login_name = login_string[login_name_index:login_name_end]
                            password_name_index = input_string.find('name="') + 6
                            password_name_end = password_name_index + input_string[password_name_index:].find('"')
                            self.password_name = input_string[password_name_index:password_name_end]
                            
                            
                            
                            for item in self.login_form:
                                print item                    
            self.action = soup.find('form').get('action')
        crawledPage = Page(link_list, html_text, self.login_url)
        return crawledPage


    # Parses domain/robots.txt for links and calls searchInit
    def robotSearch(self):
        beginning_url = self.starting_url
        try:
            robot_text = self.requester.get(beginning_url + "/robots.txt")
        except:
            return
        allow_links = robotParse(robot_text, 'Allow: ')
        disallow_links = robotParse(robot_text, 'Disallow: ')
        parsed_links = allow_links + disallow_links
        for link in parsed_links:
            
            # 
            self.searchInit(beginning_url + link)
            self.starting_url = beginning_url
        # Parse for lines with disallow, then do initial_url/path
        # Option 1 call searchInit on all initial_url/path individually (I like this one)
        # Option 2 store all intial_url/path in stack for searchInturn


    def subdomainSearch(self):
        beginning_url = self.starting_url
        subdomain_text = open("subdomains-100.txt", 'r')
        subdomains = subdomain_text.read().split('\n')
        del subdomains[-1]
        parsed_domain = urlparse(beginning_url)
        for domain in subdomains:
            domain_to_search = parsed_domain.scheme + '://' + domain + '.' + parsed_domain.netloc
            
            self.searchInit(domain_to_search)
            self.starting_url = beginning_url

        return

    def robotParse(self, page, delim):
        filter_links = page.split(delim)
        parsable_links = {}
        for link in filter_links:
            if link.startswith('/'):
                endindex = link.find('\n')
                domain = link[:endindex]
                parsable_links[domain] = domain
        return parsable_links.keys()


    # Creates the reverse of a string
    def reverse(self, string):
        return string[::-1]


    # Converts a string into leet speak
    def leetSpeak(self, string):
        leet = {"a": "4", "e": "3", "l": "1", "t": "7", "o": "0"}
        for i in range(len(string)):
            if string[i] in leet:
                string = string[:i] + leet[string[i]] + string[i+1:]
        return string


    # Parses html pages from the queue and creates a list:
    # [word, reversed, leetSpeak] to be placed into a dictionary of words
    def parser(self):
        while True:
            if self.parserQueue.empty():
                return
            page = self.parserQueue.get()
            
            soup = BeautifulSoup(page.html_text, 'html.parser')
            # Get all strings
            word_list = soup.get_text().replace("'", '').replace('"', '') \
                .replace(',','').replace(';','').split()
            for element in word_list:
                if ':' in element:
                    continue
                self.word_dict.append(element)
                self.word_dict.append(self.reverse(element))
                self.word_dict.append(self.leetSpeak(element))
        return

#crawl = Crawler(3,3,0,False,False)
#crawl.searchInit("http://forrescue.net")
#
#robotSearch()
#subdomainSearch()
#parser()
# robotSearch()
# OR Call bruteForce func
#
#
#

from page import Page
from url_node import URL_Node
from Queue import Queue
from Stack import Stack
import requests
from bs4 import BeautifulSoup
# from threading import Thread
from Requester import Requester

# Variables from config
search_flag = 0 if input("BFS (0) or DFS (1): ") == 0 else 1
max_pages = input("Max pages: ")
max_depth = input("Max depth: ")

# Queue for page objects
parserQueue = Queue()

# Dictionary of keywords
word_dict = {}

# Dictoinary of visited Linkes
link_dict = {}

# Starting url
starting_url = "http://shop.nhl.com"
#starting_url = "http://austinchildrensacademy.org"
main_domain = starting_url.split("//")[1].split(".")[0]
requester = Requester(starting_url)
def searchInit(initial_url):
    # :ssword:q Makes q/s
    # Add first url to q/s
    form_url = ""
    link_dict[initial_url] = initial_url
    first_url = URL_Node(initial_url+'/', 0)
    if search_flag == 0:
        crawlerQueue = Queue()
        crawlerQueue.put(first_url)
    else:
        crawlerStack = Stack()
        crawlerStack.push(first_url)
    # Page counter
    counter = max_pages
    # Make Q for Parser
    while counter >= 0:
        # Take from q/s and check for domain, if it does not continue
        # Also added if queue was empty to cover edge case of q/s hanging when max_pages < available pages
        if search_flag == 0:
            if crawlerQueue.empty():
                break
            nextUrl = crawlerQueue.get()
        else:
            if crawlerStack.is_empty():
                break
            nextUrl = crawlerStack.pop()

        # Stay within the domain of initial url
        # Needs to work for AA.BBB.CCC.com
        print nextUrl.url
        if nextUrl.url.split("//")[1].split(".")[0] != main_domain:
            continue
        # Call search and return page object
        # print "Url is "
        # print nextUrl.url
        next_page = search(nextUrl)
        # print nextUrl.url
        # Check if object was empty from page error Edit to check for response
        if next_page:
            if next_page.url_list and nextUrl.depth < max_depth:
                if next_page.login_url and not form_url:
                    form_url = next_page.login_url
                # Put all links into q/s
                for url_item in next_page.url_list:
                    next_node = URL_Node(url_item, nextUrl.depth + 1)
                    # Ignore repeated links when crawling
                    if link_dict.get(next_node.url) is None:
                        link_dict[next_node.url] = next_node.url
                        if search_flag == 0:
                            crawlerQueue.put(next_node)
                        else:
                            crawlerStack.push(next_node)
            parserQueue.put(next_page)
        counter = counter - 1
    return


# Searches url and returns a "page" of text and links
def search(domain):
    # Get Text
    # Change  requests to use own get
    #html_text = requests.request('GET', domain.url, timeout=7).text
    html_text = requester.get(domain.url).response_body
    if html_text == -1:
        return None
    soup = BeautifulSoup(html_text, 'html.parser')
    # Get links
    link_list = []
    for link in soup.find_all('a'):
        #print link
        if link.get('href') is not None and "http" in link.get('href'):
            link_list.append(link.get('href'))

    # Check for login
    login_url = ''
    if soup.find_all(type='password'):
        login_url = domain.url
    crawledPage = Page(link_list, html_text, login_url)
    return crawledPage


# Parses domain/robots.txt for links and calls searchInit
def robotSearch():
    robot_text = requests.request('GET', starting_url + "/robots.txt").text
    allow_links = robotParse(robot_text, 'Allow: ')
    disallow_links = robotParse(robot_text, 'Disallow: ')
    parsed_links = allow_links + disallow_links
    for link in parsed_links:
        print link
        # print "calling searchInit"
        searchInit(starting_url + link)
    # Parse for lines with disallow, then do initial_url/path
    # Option 1 call searchInit on all initial_url/path individually (I like this one)
    # Option 2 store all intial_url/path in stack for searchInit
    return


def subdomainSearch():
    subdomain_text = open("subdomains-100.txt", 'r')
    subdomains = subdomain_text.read().split('\n')
    del subdomains[-1]
    domain_index = starting_url.find('.')
    for domain in subdomains:
        domain_to_search = "http://" + domain + starting_url[domain_index:]
        print domain_to_search
        searchInit(domain_to_search)

    return

def robotParse(page, delim):
    filter_links = page.split(delim)
    parsable_links = {}
    for link in filter_links:
        if link.startswith('/'):
            endindex = link.find('\n')
            domain = link[:endindex]
            parsable_links[domain] = domain
    return parsable_links.keys()


# Creates the reverse of a string
def reverse(string):
    return string[::-1]


# Converts a string into leet speak
def leetSpeak(string):
    leet = {"a": "4", "e": "3", "l": "1", "t": "7", "o": "0"}
    for i in range(len(string)):
        if string[i] in leet:
            string = string[:i] + leet[string[i]] + string[i+1:]
    return string


# Parses html pages from the queue and creates a list:
# [word, reversed, leetSpeak] to be placed into a dictionary of words
def parser():
    while True:
        if parserQueue.empty():
            for key in word_dict.keys():
                print key
                continue
            return
        page = parserQueue.get()
        print parserQueue.qsize()
        soup = BeautifulSoup(page.html_text, 'html.parser')
        # Get all strings
        word_list = soup.get_text().replace("'", '').replace('"', '') \
            .replace(',','').replace(';','').split()
        for element in word_list:
            if (len(element) < 6) or (len(element) > 15) or (':' in element):
                continue
            word_dict[element] = {element, reverse(element), leetSpeak(element)}
    return

searchInit(starting_url)
#robotSearch()
#subdomainSearch()
parser()
# robotSearch()
# OR Call bruteForce func

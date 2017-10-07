from page import Page
from url_node import URL_Node
from Queue import Queue
from Stack import Stack
import requests
from bs4 import BeautifulSoup
# from threading import Thread

# Variables from config
search_flag = 0 if input("BFS (0) or DFS (1): ") == 0 else 1
max_pages = input("Max pages: ") 
max_depth = input("Max depth: ") 

# Queue for page objects
parserQueue = Queue()

# Dictionary of keywords
word_dict = {}

#Starting url
initial_url = "http://www.youtube.com"

# Form url
form_url = ""

def searchInit():
    #:ssword:q Makes q/s
    # Add first url to q/s
    first_url = URL_Node(initial_url, 0)
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
                return
            nextUrl = crawlerQueue.get()
        else:
            if crawlerStack.is_empty():
                return
            nextUrl = crawlerStack.pop()

        # Stay within the domain of initial url
        if nextUrl.url.split(".")[1] != initial_url.split(".")[1]:
            continue        
        # Call search and return page object
        print nextUrl.url
        next_page = search(nextUrl)
        # Check if object was empty from page error Edit to check for response
        if next_page.url_list and nextUrl.depth < max_depth:
            # Put all links into q/s
            for url_item in next_page.url_list:
                #print url_item
                next_node = URL_Node(url_item, nextUrl.depth + 1)
                if search_flag == 0:
                    crawlerQueue.put(next_node)
                else:
                    crawlerStack.push(next_node)
        parserQueue.put(next_page)
        counter = counter - 1
    return


# Searches url and returns a "page" of text and links
def search(link):
    # Get Text
    html_text = requests.request('GET', link.url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    # Get links
    link_list = []
    for link in soup.find_all('a'):
        if link.get('href') is not None and "http" in link.get('href'):
            link_list.append(link.get('href'))

    # Check for login
    login_url = ''
    if soup.find_all(type='password'):
        login_url = link
    crawledPage = Page(link_list, html_text, login_url)
    return crawledPage

# Parses domain/robots.txt for links and calls searchInit
def robotSearch():
    robot_text = requests.request('GET',initial_url+"/robots.txt").text
    #Parse for lines with disallow, then do initial_url/path
    #Option 1 call searchInit on all initial_url/path individually (I like this one)
    #Option 2 store all intial_url/path in stack for searchInit
    return

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
        page = parserQueue.get()
        print parserQueue.qsize()
        soup = BeautifulSoup(page.html_text, 'html.parser')
        print soup.title
        # Get all strings
        word_list = soup.get_text().split()
        for element in word_list:
            word_dict[element] = {element, reverse(element), leetSpeak(element)}
        if parserQueue.empty():
            return
    return


searchInit()
parser()
#robotSearch()
# OR Call bruteForce func

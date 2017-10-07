from page import Page
from url_node import URL_Node
from Queue import Queue
from Stack import Stack
import requests
from bs4 import BeautifulSoup
# from threading import Thread

# Read from crawler.conf

# Crawl url from stdin (?)

# BFS
# Search entire page for links, return array of links to search
# Use queue to store links to crawl

# DFS
# Search entire page for links, return array of links to search
# Use stack to store links to crawl

# Create threads that crawl from urls in queue/stack
# While crawling look for login form page (?)

# Variables from config
max_pages = 5
max_depth = 5
search_flag = 1

# Queue for page objects
parserQueue = Queue()

# Dictionary of keywords
word_dict = {}

# Form url
form_url = "http://www.youtube.com"


def searchInit():
    # Makes q/s
    # Add first url to q/s
    first_url = URL_Node(form_url, 0)
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
        if search_flag == 0:
            nextUrl = crawlerQueue.get()
        else:
            nextUrl = crawlerStack.pop()
        # Call search and return page object
        next_page = search(nextUrl)
        # Check if object was empty from page error Edit to check for response
        if next_page.url_list and nextUrl.depth < max_depth:
            # Put all links into q/s
            for url_item in next_page.url_list:
                print url_item
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
def Parser():
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
Parser()
# OR Call bruteForce func

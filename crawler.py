import page
import Queue
import Stack
import requests
from bs4 import BeautifulSoup
from threading import Thread

#Read from crawler.conf

#Crawl url from stdin (?)

#BFS
#Search entire page for links, return array of links to search
#Use queue to store links to crawl

#DFS
#Search entire page for links, return array of links to search
#Use stack to store links to crawl

#Create threads that crawl from urls in queue/stack
#While crawling look for login form page (?)

#Variables from config
max_pages = 0
max_depth = 0
search_flag = 0

#Queue for page objects
parserQueue = Queue.Queue()

#Dictionary of keywords
word_dict = {}

#Form url
form_url = ""

def searchInit():
    #Makes q/s
    #Add first url to q/s
    #Page counter
    #Make Q for Parser
    while counter != 0:
        #Take from q/s and check for domain, if it does not continue
        #Call search and return page object
        #Check if object was empty from page error
        #Put all links into q/s
        break
    return

#Creates the reverse of a string
def reverse(string):
    result = ""
    for char in string:
        resulti+= char
    return result

#Converts a string into leet speak
def leetSpeak(string):
    leet = {"a" : "4", "e" : "3", "l" : "1", "t" : "7", "o" : "0"}
    for i in range(string):
        if string(i) in leet
            string(i) = leet[string(i)]
    return string

#Parses html pages from the queue and creates a list:
# [word, reversed, leetSpeak] to be placed into a dictionary of words
def Parser():
    while True:
        page = parserQueue.get()
        soup = BeautifulSoup(page.html_text, 'html.parser')
        #Get all strings
        word_list = soup.get_text().split()
        for element in word_list:
            word_dict[element] = {element, reverse(element), leetSpeak(element)}
    return

#OR Call bruteForce func

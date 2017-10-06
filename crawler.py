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

#Queue for page objects
parserQueue = Queue.Queue()

#Dictionary of keywords
word_dict = {}

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

#Create threads that parse texts returned from crawlers (?)

def Parser():
    while True:
        page = parserQueue.get()
        soup = BeautifulSoup(html_doc, 'html.parser')
        #Get all strings
        word_list = soup.get_text().split()
        for element in word_list:
            word_dict[element] = element
    return
#Save parsed keywords to a file: url_passwords.txt








#Exec Form bruteforcer with file
#OR Call bruteForce func

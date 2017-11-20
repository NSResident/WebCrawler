from Tkinter import *
from crawler import Crawler
root = Tk()
crawler_object = None
def show_words():
    if crawler_object:
        BF_text = Text(root)
        BF_text.grid(row = 9, columnspan = 2, sticky = N+S+E+W)
        filtered_dict = [word for n,word in enumerate(crawler_object.word_dict) if word not in crawler_object.word_dict[:n]]
        crawler_object.word_dict = filtered_dict
        for word in filtered_dict:
            BF_text.insert(END, word.encode('utf-8') + '\n')
def bruteforce_page(names):
    global crawler_object
    BF_text = Text(root)
    print crawler_object
    print crawler_object.login_url
    print crawler_object.word_dict
    print crawler_object.action
    name_list = []
    if names:
        name_list = names.split(',')
    print len(name_list)
    BF_text.grid(row = 9, columnspan = 2)
    BF_text.insert(END, "Attempted:\n")
    try:
        success= crawler_object.requester.bruteForceInit(crawler_object.login_url, name_list,crawler_object.word_dict, crawler_object.action, crawler_object.login_name, crawler_object.password_name, crawler_object.login_form)
        print crawler_object.requester.attempt_values
        BF_text.insert(END, "Tried " + str(len(crawler_object.requester.attempt_values)) + " credentials")
        if success:
            BF_text.insert(END, "\n Successful login with " + str(success))
    except:
        BF_text.insert(END, "Error Bruteforcing Page. please modify your search")
def crawl(page_max, depth_max, search_type, subdom, robots, initial_url):
    global BF_text
    global crawler_object
    crawler_object = Crawler(int(page_max),int(depth_max), int(search_type),bool(subdom), bool(robots))
    visited = crawler_object.searchStart(initial_url)
    BF_text = Text(root)
    BF_text.grid(row = 9, columnspan = 2, sticky = N+S+E+W)
    for link in visited:
        BF_text.insert(END, str(link) +"\n")

for i in range(10):
    root.grid_columnconfigure(i, weight = 2)
    root.grid_rowconfigure(i, weight = 2)
url = Label(root, text = "URL")
max_depth = Label(root,text="Max Depth")
max_pages = Label(root, text = "Max Pages")
extra_users = Label(root, text = "Extra Users")
url_entry = Entry(root)
depth_entry = Entry(root)
pages_entry = Entry(root)
users_entry = Entry(root)
url.grid(row = 0,sticky = N+S+E+W)
max_depth.grid(row = 1, sticky = N+S+E+W)
max_pages.grid(row = 2, sticky = N+S+E+W)
extra_users.grid(row = 3, sticky = N+S+E+W)
url_entry.grid(row = 0, column = 1, sticky = N+S+E+W)
depth_entry.grid(row = 1, column = 1,sticky = N+S+E+W)
pages_entry.grid(row = 2, column = 1,sticky = N+S+E+W)
users_entry.grid(row = 3, column = 1, sticky = N+S+E+W)
subdomains_button = IntVar()
Checkbutton(root, text = "Subdomains", variable = subdomains_button).grid(row = 4, sticky = W)
robots_txt_button = IntVar()
Checkbutton(root, text = "Robots.txt", variable = robots_txt_button).grid(row = 4, column = 1, sticky = W)
dfsbfs_button = IntVar()
Checkbutton(root, text = "DFS/BFS", variable = dfsbfs_button).grid(row = 5, sticky = W)
crawl_button = Button(root, text = "Crawl", command = lambda: crawl(pages_entry.get(), depth_entry.get(), dfsbfs_button.get(), subdomains_button.get(), robots_txt_button.get(), url_entry.get()))
crawl_button.grid(row = 6,columnspan = 2, sticky = N+S+E+W)
BF_button = Button(root, text = "BruteForce", command = lambda: bruteforce_page(users_entry.get()))
words_button = Button(root, text = "Word Bank", command = lambda: show_words())
words_button.grid(row = 8, columnspan = 2, sticky = N+S+E+W)
BF_button.grid(row = 7, columnspan = 2, sticky = N+S+E+W)
root.mainloop()

